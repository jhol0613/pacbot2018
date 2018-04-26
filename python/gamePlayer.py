#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *
import time
import atexit

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11293)

FREQUENCY = 50

# File containing action sequence for the robot
ACTION_SEQUENCE_FILES = ["paths/path1.txt"]

# Constants for rotations
ROTATIONAL_CORRECTION_CONSTANT = 1.1 # adjustment factor for unequal turning
ROTATIONAL_SPEED = 40 # speed at which rotations occur
ODOMETRY_LEFT_TURN_THRESHOLD = 210 # odometer cutoff for finishing left turn
ODOMETRY_RIGHT_TURN_THRESHOLD = 210 # odometer cutoff for finishing right turn

# Constants for pause
PAUSE_TIME = 0.5 # length of a typical pause

# Constants for straight motion
FORWARD_SPEED = 35 # nominal forward movement speed
FORWARD_OMEGA_CORRECTION = 4 # correction for unequal friction
FRONT_SENSOR_THRESHOLD_1 = 13 # minimum sensor value before slowing forward motion
FRONT_SENSOR_THRESHOLD_2 = 5 # minimum sensor value before stopping forward motion
INTER_THRESHOLD_SPEED = 15 # speed to travel after activating first front threshold
SENSOR_CASE_THRESHOLD = 11 # max sensor reading that is considered when centering path
SENSOR_CASE_MIN = 3.5 # assume sensor readings below this are garbage and don't consider
SENSOR_TARGET = 7.0 # target value that sensors try to return to
P_MULTIPLIER = 5.0 # this is multiplied by calculated position correction factor to determine omega
D_MULTIPLIER = 9.0 # this is multiplied by calculated direction correction factor to determine omega

# Constants for initial move (odometered forward motion)
ODOMETRY_INITIAL_MOVE_THRESHOLD = 360 # odometer cutoff for finishing initial forward motion
FORWARD_CORRECTION_CONSTANT = 1 # adjustment for unequal motion

# Constants for bump recovery
BUMP_RECOVERY_OMEGA = 17 # should be positive. Potentially negated based on side of bump
BUMP_RECOVERY_VELOCITY = -28 # should be negative because you want to move backwards
ODOMETRY_BUMP_RECOVERY_THRESHOLD = 280 # Odometry measured off the outside wheel
BUMP_RECOVERY_TIMEOUT = 1 # amount of time (seconds) before bump recovery times out

class GamePlayer(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.BUMPER, MsgType.LIGHT_STATE, MsgType.ULTRASONIC_ARRAY, MsgType.ENCODER_REPORT]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)

        r = open(ACTION_SEQUENCE_FILES[0], "r")
        self.action_sequence = r.read().split('\n')
        print("Action Sequence: ", self.action_sequence)
        
        self.paused = True # Flag that tracks whether the game is paused
        self.action_complete = False # Flag that tells whether to continue same action or move to next
        self.action_started = False # Flag that tracks whether an action is in progress
        
        self.distance = None # UltrasonicArray message with all measured distances
        self.odom_reading = None # EncoderReport message with encoder clicks since encoder BEGIN command sent
        
        self.bumper = None # Bumper message showing whether left or right was hit first
        self.recoveringFromBump = False # Flag shows whether robot is currently recovering from bump
        self.bumpRecoveryStarted = False # Flag shows whether robot has started bump recovery

        self.cursor = 0 # Marks position in action sequence

        self.timer = 0 # Can be used by subroutines that use time as an exit condition

        print("GamePlayer running")

        # self.csvOut = open("p_test.csv", "w+")

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        if msg_type == MsgType.LIGHT_STATE:
            if msg.mode == LightState.RUNNING:
                self.paused = False
            elif msg.mode == LightState.PAUSED:
                self.paused = True

        elif msg_type == MsgType.ULTRASONIC_ARRAY:
            self.distance = msg
            # print("\n"*20)
            # print("Front Center: ", self.distance.front_center)
        elif msg_type == MsgType.ENCODER_REPORT:
            self.odom_reading = msg

        elif msg_type == MsgType.BUMPER:
            print("bump message received...")
            if not self.recoveringFromBump: # only reads new bump events once you've recovered
                print("bump registered!")
                self.bumper = msg
                self.recoveringFromBump = True

    def tick(self):
        moveCommand = Twist()

        if self.paused:
            print("Game paused")
            moveCommand.velocity = 0
            moveCommand.omega = 0
        else:
            # Advance cursor if action is complete
            if self.action_complete:
                self.cursor += 1
                self.action_complete = False
                self.action_started = False
            # Stop movement if completed action_sequence
            if self.cursor >= len(self.action_sequence):
                moveCommand.velocity = 0
                moveCommand.omega = 0
            else:
                # Case for each potential action
                action = self.action_sequence[self.cursor]
                if self.recoveringFromBump:
                    moveCommand = self.bumpRecover()
                    print("Move Command Omega: ", moveCommand.omega())
                elif action == 'TURN_90_LEFT':
                    moveCommand = self.turn90Left()
                elif action == 'TURN_90_RIGHT':
                    moveCommand = self.turn90Right()
                elif action == 'GO_STRAIGHT':
                    moveCommand = self.goStraight()
                elif action == 'INITIAL_MOVE':
                    moveCommand = self.initialMove()
                elif action == 'PAUSE':
                    moveCommand = self.pause()

        moveCommand = moveCommand.SerializeToString()
        self.write(moveCommand, MsgType.TWIST)

    # List of subroutines that the pacbot can enter
    def turn90Left(self):
        twist = Twist()
        if not self.action_started:
            self.action_started = True
            encoderControl = EncoderControl()
            encoderControl.command = EncoderControl.BEGIN
            self.write(encoderControl.SerializeToString(), MsgType.ENCODER_CONTROL)
        if self.turn90LeftExitCondition():
            self.action_complete = True
            encoderControl = EncoderControl()
            encoderControl.command = EncoderControl.RESET
            self.write(encoderControl.SerializeToString(), MsgType.ENCODER_CONTROL)
            twist.velocity = 0
            twist.omega = 0
        else:
            twist.velocity = 0
            twist.omega = 0
            if self.odom_reading:
                twist.velocity += int((self.odom_reading.left - self.odom_reading.right) * ROTATIONAL_CORRECTION_CONSTANT)
                twist.omega = -ROTATIONAL_SPEED
        return twist
        # Remember to add the opposite correction from turn90right!!!

    def turn90Right(self):
        twist = Twist()
        if not self.action_started:
            self.action_started = True
            encoderControl = EncoderControl()
            encoderControl.command = EncoderControl.BEGIN
            self.write(encoderControl.SerializeToString(), MsgType.ENCODER_CONTROL)
        if self.turn90RightExitCondition():
            self.action_complete = True
            encoderControl = EncoderControl()
            encoderControl.command = EncoderControl.RESET
            self.write(encoderControl.SerializeToString(), MsgType.ENCODER_CONTROL)
            twist.velocity = 0
            twist.omega = 0
        else:
            twist.velocity = 0
            twist.omega = 0
            if self.odom_reading:
                twist.velocity += int((self.odom_reading.right - self.odom_reading.left) * ROTATIONAL_CORRECTION_CONSTANT)
                twist.omega = ROTATIONAL_SPEED
        return twist

    def goStraight(self):

        twist = Twist()

        if not self.action_started:
            self.action_started = True
        if self.goStraightExitCondition():
            self.action_complete = True
            twist.velocity = 0
            twist.omega = 0
        else:
            case = self.checkCase()
            numActiveSensors = sum(case)
            if numActiveSensors > 0:
                # Calculate pCorrection factor
                sensorArray = [self.distance.front_left, self.distance.front_right, self.distance.rear_left, self.distance.rear_right]
                pCorrectionFactor = 0
                for sensorIndex, active in enumerate(case):
                    if active:
                        # Reverse the correction for rear sensors
                        if sensorIndex % 2 == 0:
                            pCorrectionFactor += (SENSOR_TARGET - sensorArray[sensorIndex])
                        else:
                            pCorrectionFactor -= (SENSOR_TARGET - sensorArray[sensorIndex])
                pCorrectionFactor = int((pCorrectionFactor / numActiveSensors) * P_MULTIPLIER + 0.5)

                # Calculate dCorrection factor
                dCorrectionFactor = 0
                for sensorIndex, active in enumerate(case):
                    if active:
                        # Reverse the correction for rear sensors
                        if sensorIndex == 0 or sensorIndex == 3:
                            dCorrectionFactor += (SENSOR_TARGET - sensorArray[sensorIndex])
                        else:
                            dCorrectionFactor -= (SENSOR_TARGET - sensorArray[sensorIndex])
                dCorrectionFactor = int((dCorrectionFactor / numActiveSensors) * D_MULTIPLIER + 0.5)
            else:
                pCorrectionFactor = 0
                dCorrectionFactor = 0
            
            # self.csvOut.write(str(round(self.distance.front_left, 2)) + ",")
            # self.csvOut.write(str(round(self.distance.front_right, 2)) + ",")
            # self.csvOut.write(str(round(self.distance.rear_left, 2)) + ",")
            # self.csvOut.write(str(round(self.distance.rear_right, 2)) + ",")
            # self.csvOut.write(str(pCorrectionFactor) + ",")
            # self.csvOut.write(str(dCorrectionFactor) + "\n")

            if self.distance.front_center > FRONT_SENSOR_THRESHOLD_1:
                twist.velocity = FORWARD_SPEED
                twist.omega = FORWARD_OMEGA_CORRECTION + pCorrectionFactor + dCorrectionFactor
            else:
                twist.velocity = INTER_THRESHOLD_SPEED
                # twist.omega = FORWARD_OMEGA_CORRECTION + pCorrectionFactor + dCorrectionFactor
                twist.omega = int(float(INTER_THRESHOLD_SPEED)/FORWARD_SPEED) * (FORWARD_OMEGA_CORRECTION + pCorrectionFactor + dCorrectionFactor)

        return twist

    # case takes form [front_left, front_right, rear_left, rear_right]
    def checkCase(self):
        a = self.distance.front_left < SENSOR_CASE_THRESHOLD and self.distance.front_left > SENSOR_CASE_MIN
        b = self.distance.front_right < SENSOR_CASE_THRESHOLD and self.distance.front_right > SENSOR_CASE_MIN
        c = self.distance.rear_left < SENSOR_CASE_THRESHOLD and self.distance.rear_left > SENSOR_CASE_MIN
        d = self.distance.rear_right < SENSOR_CASE_THRESHOLD and self.distance.rear_right > SENSOR_CASE_MIN
        case = [a, b, c, d]
        # print("Case (in checkCase): ", case)
        return case

    # This is the only subroutine that can interrupt another
    def bumpRecover(self):
        print("bump recovering")
        twist = Twist()
        if not self.bumpRecoveryStarted:
            self.bumpRecoveryStarted = True
            self.timer = time.time()
            encoderControl = EncoderControl()
            encoderControl.command = EncoderControl.BEGIN
            self.write(encoderControl.SerializeToString(), MsgType.ENCODER_CONTROL)
        if self.bumpRecoverExitCondition() or (time.time() - self.timer) > BUMP_RECOVERY_TIMEOUT:
            self.recoveringFromBump = False
            self.bumpRecoveryStarted = False
            encoderControl = EncoderControl()
            encoderControl.command = EncoderControl.RESET
            self.write(encoderControl.SerializeToString(), MsgType.ENCODER_CONTROL)
            twist.velocity = 0
            twist.omega = 0
        else:
            twist.velocity = 0
            twist.omega = 0
            if self.odom_reading:
                if self.bumper.side == Bumper.LEFT:
                    twist.omega = BUMP_RECOVERY_OMEGA
                else:
                    twist.omega = -BUMP_RECOVERY_OMEGA
                twist.velocity = BUMP_RECOVERY_VELOCITY
        return twist

    # May require two separate parts
    def initialMove(self):
        twist = Twist()
        if not self.action_started:
            self.action_started = True
            encoderControl = EncoderControl()
            encoderControl.command = EncoderControl.BEGIN
            self.write(encoderControl.SerializeToString(), MsgType.ENCODER_CONTROL)
        if self.initialMoveExitCondition():
            self.action_complete = True
            encoderControl = EncoderControl()
            encoderControl.command = EncoderControl.RESET
            self.write(encoderControl.SerializeToString(), MsgType.ENCODER_CONTROL)
            twist.velocity = 0
            twist.omega = 0
        else:
            twist.velocity = 0
            twist.omega = 0
            if self.odom_reading:
                twist.velocity = FORWARD_SPEED
                twist.omega = FORWARD_OMEGA_CORRECTION + int((self.odom_reading.right - self.odom_reading.left) * FORWARD_CORRECTION_CONSTANT)
        return twist

    def pause(self):

        # self.csvOut.close()

        twist = Twist()
        if not self.action_started:
            self.action_started = True
            self.timer = time.time()
        if self.pauseExitCondition():
            self.action_complete = True
        twist.velocity = 0
        twist.omega = 0
        return twist

    # Checks specified conditions and returns a boolean stating whether
    # a subroutine should end
    def turn90LeftExitCondition(self):
        if self.odom_reading:
            print("Left odom reading: ", self.odom_reading.left)
            print("Right odom reading: ", self.odom_reading.right)
            if self.odom_reading.right > ODOMETRY_LEFT_TURN_THRESHOLD:
                return True
        return False

    def turn90RightExitCondition(self):
        if self.odom_reading:
            print("Left odom reading: ", self.odom_reading.left)
            print("Right odom reading: ", self.odom_reading.right)
            if self.odom_reading.right > ODOMETRY_RIGHT_TURN_THRESHOLD:
                return True
        return False

    def goStraightExitCondition(self):
        # print("Front distance: ", self.distance.front_center)
        # return False
        if self.distance:
            print("Front sensor: ", self.distance.front_center)
            return self.distance.front_center < FRONT_SENSOR_THRESHOLD_2
        else:
            print("No front sensor value")
            return False

    def bumpRecoverExitCondition(self):
        if self.odom_reading:
            # print("Left odom reading: ", self.odom_reading.left)
            # print("Right odom reading: ", self.odom_reading.right)
            if self.bumper.side == Bumper.LEFT: # measure odometry off outer wheel
                if self.odom_reading.right > ODOMETRY_BUMP_RECOVERY_THRESHOLD:
                    return True
            else:
                if self.odom_reading.left > ODOMETRY_BUMP_RECOVERY_THRESHOLD:
                    return True
        return False

    def initialMoveExitCondition(self):
        if self.odom_reading:
            print("Left odom reading: ", self.odom_reading.left)
            print("Right odom reading: ", self.odom_reading.right)
            if self.odom_reading.right > ODOMETRY_INITIAL_MOVE_THRESHOLD:
                return True
        return False

    def pauseExitCondition(self):
        return (time.time() - self.timer) > PAUSE_TIME

def main():
    module = GamePlayer(ADDRESS, PORT)
    time.sleep(1)
    module.run()

if __name__ == "__main__":
    main()
