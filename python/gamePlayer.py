#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *
import time

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11293)

FREQUENCY = 40

# File containing action sequence for the robot
ACTION_SEQUENCE_FILES = ["paths/testPath.txt"]

# Constants for rotations
ROTATIONAL_CORRECTION_CONSTANT = 1 # adjustment factor for unequal turning
ROTATIONAL_SPEED = 40 # speed at which rotations occur
ODOMETRY_LEFT_TURN_THRESHOLD = 250 # odometer cutoff for finishing left turn
ODOMETRY_RIGHT_TURN_THRESHOLD = 280 # odometer cutoff for finishing right turn

# Constants for pause
PAUSE_TIME = 0.5 # length of a typical pause

# Constants for straight motion
FORWARD_SPEED = 40 # nominal forward movement speed
FORWARD_OMEGA_CORRECTION = 4 # correction for unequal friction
FRONT_SENSOR_THRESHOLD = 8.0 # minimum sensor value before stopping forward motion
SENSOR_CASE_THRESHOLD = 12 # max sensor reading that is considered when centering path

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

        self.cursor = 0 # Marks position in action sequence

        self.timer = 0 # Can be used by subroutines that use time as an exit condition
        print("GamePlayer running")

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        if msg_type == MsgType.LIGHT_STATE:
            if msg.mode == LightState.RUNNING:
                self.paused = False
            elif msg.mode == LightState.PAUSED:
                self.paused = True

        elif msg_type == MsgType.ULTRASONIC_ARRAY:
            self.distance = msg
        elif msg_type == MsgType.ENCODER_REPORT:
            self.odom_reading = msg
        elif msg_type == MsgType.BUMPER:
            self.bumper = msg

    def tick(self):
        start = time.time()
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

                # '''......................TEMPORARY TEST CODE START....................'''

                # print('\n' * 20)
                # print("Front Left: ", round(self.distance.front_left, 2))
                # print("Front Right: ", round(self.distance.front_right, 2))
                # print("Rear Left: ", round(self.distance.rear_left, 2))
                # print("Rear Right: ", round(self.distance.rear_right,2))

                # '''......................TEMPORARY TEST CODE END......................'''

            else:
                # Case for each potential action
                action = self.action_sequence[self.cursor]
                if self.bumper:
                    moveCommand = self.bumpRecover()
                elif action == 'TURN_90_LEFT':
                    moveCommand = self.turn90Left()
                elif action == 'TURN_90_RIGHT':
                    moveCommand = self.turn90Right()
                elif action == 'GO_STRAIGHT':
                    moveCommand = self.goStraight()
                elif action == 'INITIAL_TURN':
                    moveCommand = self.initialTurn()
                elif action == 'PAUSE':
                    moveCommand = self.pause()

        moveCommand = moveCommand.SerializeToString()
        self.write(moveCommand, MsgType.TWIST)

        # print("Tick time: ", time.time() - start)

    # List of subroutines that the pacbot can enter
    def turn90Left(self):
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

        case = self.checkCase()

        # if not self.action_started:
        #     self.action_started = True

        # if self.goStraightExitCondition():
        #     self.action_complete = True
        #     twist.velocity = 0
        #     twist.omega = 0
        # else:
        #     twist.velocity = FORWARD_SPEED
        #     twist.omega = FORWARD_OMEGA_CORRECTION
        # return twist
        twist.velocity = 0
        twist.omega = 0
        print("Case: ", bin(case))
        return twist

    # case is a binary number with following structure
    # first digit: front left sensor active
    # second digit: front right sensor active
    # third digit: rear left sensor active
    # fourth digit: rear right sensor active
    def checkCase(self):
        a = 8 * int(self.distance.front_left < SENSOR_CASE_THRESHOLD)
        b = 4 * int(self.distance.front_right < SENSOR_CASE_THRESHOLD)
        c = 2 * int(self.distance.rear_left < SENSOR_CASE_THRESHOLD)
        d = 1 * int(self.distance.rear_right < SENSOR_CASE_THRESHOLD)
        case = a + b + c + d
        return case

    # This is the only subroutine that can interrupt another
    def bumpRecover(self):
        twist = Twist()
        twist.velocity = 0
        twist.omega = 0
        return twist

    # May require two separate parts
    def initialTurn(self):
        '''TODO'''
        return

    def pause(self):
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
        print("Front distance: ", self.distance.front_center)
        # return False
        return self.distance.front_center < FRONT_SENSOR_THRESHOLD

    def bumpRecoverExitCondition(self):
        '''TODO'''
        return True

    def initialTurnExitCondition(self):
        '''TODO'''
        return True

    def pauseExitCondition(self):
        return (time.time() - self.timer) > PAUSE_TIME


def main():
    module = GamePlayer(ADDRESS, PORT)
    time.sleep(1)
    module.run()

if __name__ == "__main__":
    main()
