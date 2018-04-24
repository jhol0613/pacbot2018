#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *
import time

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11293)

FREQUENCY = 40

ACTION_SEQUENCE = ['GO_STRAIGHT', 'TURN_90_RIGHT']

ROTATIONAL_CORRECTION_CONSTANT = 3

class GamePlayer(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.BUMPER, MsgType.LIGHT_STATE, MsgType.ULTRASONIC_ARRAY, MsgType.ENCODER_REPORT]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        
        self.paused = True # Flag that tracks whether the game is paused
        self.action_complete = False # Flag that tells whether to continue same action or move to next
        self.action_started = False # Flag that tracks whether an action is in progress
        
        self.distance = None # UltrasonicArray message with all measured distances
        self.odom_reading = None # EncoderReport message with encoder clicks since encoder BEGIN command sent
        self.bumper = None # Bumper message showing whether left or right was hit first

        self.cursor = 0 # Marks position in action sequence

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
            if self.cursor >= len(ACTION_SEQUENCE):
                print("Cursor too large for some reason")
                moveCommand.velocity = 0
                moveCommand.omega = 0
            else:
                # Case for each potential action
                action = ACTION_SEQUENCE[self.cursor]
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

        self.write(moveCommand.SerializeToString(), MsgType.TWIST)

        print("Tick time: ", time.time() - start)

        # this function will get called in a loop with FREQUENCY frequency
        # wheels_msg = Twist()
        # odom_msg = EncoderControl()
        # if (not self.odom_reading) or (self.odom_reading.left > 300):
        #     odom_msg.command = EncoderControl.RESET
        #     self.serializeAndWrite(odom_msg, MsgType.ENCODER_CONTROL)
        #     time.sleep(.01)
        #     odom_msg.command = EncoderControl.BEGIN
        #     self.serializeAndWrite(odom_msg, MsgType.ENCODER_CONTROL)
        # # else:
        # #     print("Right encoder clicks: ", self.odom_reading.right)

        # wheels_msg.velocity = 20
        # wheels_msg.omega = 2
        # self.serializeAndWrite(wheels_msg, MsgType.TWIST)

        # if self.distance:
        #     print("\n" * 30)
            # print("Front Center: ", self.distance.front_center) # GOOD
            # print("Front Left: ", self.distance.front_left) # GOOD
            # print("Front Right: ", self.distance.front_right) # BAD!!!
            # print("Rear Left: ", self.distance.rear_left) #GOOD
            # print("Rear Right: ", self.distance.rear_right) #BAD!!!
        # if self.moving:
        #     # msg.velocity = 98
        #     # msg.omega = 2
        #     print("Currently moving")
        # else:
        #     print("Currently stopped")
        #     # msg.velocity = 0
        #     # msg.omega = 0
        # # msg = msg.SerializeToString()
        # # self.write(msg, MsgType.TWIST)
        


    # def serializeAndWrite(self, msg, msg_type):
    #     msg = msg.SerializeToString()
    #     self.write(msg, msg_type)

    # List of subroutines that the pacbot can enter
    def turn90Left(self):
        '''TODO'''

        # Remember to add the opposite correction from turn90right!!!
        return

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
            twist.velocity += (self.odom_reading.right - self.odom_reading.left) * int(ROTATIONAL_CORRECTION_CONSTANT)
            twist.omega = 40
        return twist

    def goStraight(self):
        twist = Twist()
        if not self.action_started:
            self.action_started = True
        # Check action
        if self.goStraightExitCondition():
            self.action_complete = True
            twist.velocity = 0
            twist.omega = 0
        else:
            twist.velocity = 60
            twist.omega = 2
        return twist

    # This is the only subroutine that can interrupt another
    def bumpRecover(self):
        '''TODO'''
        return

    # May require two separate parts
    def initialTurn(self):
        '''TODO'''
        return

    # Checks specified conditions and returns a boolean stating whether
    # a subroutine should end
    def turn90LeftExitCondition(self):
        '''TODO'''
        return True

    def turn90RightExitCondition(self):
        if self.odom_reading:
            print("Left odom reading: ", self.odom_reading.left)
            print("Right odom reading: ", self.odom_reading.right)
            if self.odom_reading.right > 240:
                return True
        return False

    def goStraightExitCondition(self):
        print("Front distance: ", self.distance.front_center)
        # return False
        return self.distance.front_center < 4

    def bumpRecoverExitCondition(self):
        '''TODO'''
        return True

    def initialTurnExitCondition(self):
        '''TODO'''
        return True

def main():
    module = GamePlayer(ADDRESS, PORT)
    time.sleep(1)
    module.run()

if __name__ == "__main__":
    main()
