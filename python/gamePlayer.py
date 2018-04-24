#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *
import time

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11293)

FREQUENCY = 10

class GamePlayer(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.BUMPER, MsgType.LIGHT_STATE, MsgType.ULTRASONIC_ARRAY, MsgType.ENCODER_REPORT]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.moving = True
        self.distance = None
        self.odom_reading = None

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # if msg_type == MsgType.BUMPER:
        #     self.moving = False
        if msg_type == MsgType.LIGHT_STATE:
            if msg.mode == LightState.RUNNING:
                self.moving = True
            elif msg.mode == LightState.PAUSED:
                self.moving = False
        elif msg_type == MsgType.ULTRASONIC_ARRAY:
            #print("received sensor readings")
            self.distance = msg
        elif msg_type == MsgType.ENCODER_REPORT:
            self.odom_reading = msg

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        wheels_msg = Twist()
        odom_msg = EncoderControl()
        if (not self.odom_reading) or (self.odom_reading.left > 300):
            odom_msg.command = EncoderControl.RESET
            self.serializeAndWrite(odom_msg, MsgType.ENCODER_CONTROL)
            time.sleep(.01)
            odom_msg.command = EncoderControl.BEGIN
            self.serializeAndWrite(odom_msg, MsgType.ENCODER_CONTROL)
        else:
            print("Left encoder clicks: ", self.odom_reading.left)

        wheels_msg.velocity = 60
        wheels_msg.omega = 2
        self.serializeAndWrite(wheels_msg, MsgType.TWIST)

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

    def serializeAndWrite(self, msg, msg_type):
        msg = msg.SerializeToString()
        self.write(msg, msg_type)

def main():
    module = GamePlayer(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
