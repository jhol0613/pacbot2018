#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11293)

FREQUENCY = 2

class GamePlayer(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = []
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        if msg_type == MsgType.MOCK_MSG:
            self.x = msg.xValue
            self.y = msg.yValue
            print("Mock message received")
        return

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        # for this mock module we will print out the current value
        msg = Twist()
        msg.velocity = 10
        msg.omega = 0
        msg = msg.SerializeToString()
        self.write(msg, MsgType.TWIST)


def main():
    module = GamePlayer(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
