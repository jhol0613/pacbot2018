#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11293)

FREQUENCY = 10

class GamePlayer(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.BUMPER, MsgType.LIGHT_STATE, MsgType.ULTRASONIC_ARRAY]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.moving = True
        self.distance = None

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

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        # for this mock module we will print out the current value
        msg = Twist()
        if self.distance:
            print("\n" * 30)
            # print("Front Center: ", self.distance.front_center)
            # print("Front Left: ", self.distance.front_left)
            print("Front Right: ", self.distance.front_right)
        #     print("Rear Left: ", self.distance.rear_left)
        #     print("Rear Right: ", self.distance.rear_right)
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

def main():
    module = GamePlayer(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
