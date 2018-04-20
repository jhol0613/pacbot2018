#!/usr/bin/env python3

import os
import robomodules as rm
from messages import message_buffers, MsgType

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11293)

FREQUENCY = 2

class GamePlayer(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.MOCK_MSG]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.x = -1
        self.y = -2

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        if msg_type == MsgType.MOCK_MSG:
            self.x = msg.xValue
            self.y = msg.yValue

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        # for this mock module we will print out the current value
        print('Current value: ({}, {})'.format(self.x, self.y))


def main():
    module = GamePlayer(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
