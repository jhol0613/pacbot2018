#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *

SERVER_ADDRESS = os.environ.get("BIND_ADDRESS", "192.168.1.81")
SERVER_PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 30

class PacbotClient(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.state = None

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module will connect to
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        # The main functionality of your code should be here
        # For now we will just print out the state
        if self.state:
            print('\n' * 100)
            print('score: {}'.format(self.state.score))
            print('lives: {}'.format(self.state.lives))
            state = 'Running' if self.state.mode == LightState.RUNNING else 'Paused'
            print('state: {}'.format(state))
            print("pacbot's location (x,y): ({},{})".format(self.state.pacman.x, self.state.pacman.y))

            print("Red ghost's location (x,y): ({},{})".format(self.state.red_ghost.x, self.state.red_ghost.y))
            state = 'Frightened' if self.state.red_ghost.state == LightState.FRIGHTENED else 'Normal'
            print('Red ghost state: {}'.format(state))

            print("Pink ghost's location (x,y): ({},{})".format(self.state.pink_ghost.x, self.state.pink_ghost.y))
            state = 'Frightened' if self.state.pink_ghost.state == LightState.FRIGHTENED else 'Normal'
            print('Pink ghost state: {}'.format(state))

            print("Blue ghost's location (x,y): ({},{})".format(self.state.blue_ghost.x, self.state.blue_ghost.y))
            state = 'Frightened' if self.state.blue_ghost.state == LightState.FRIGHTENED else 'Normal'
            print('Blue ghost state: {}'.format(state))

            print("Orange ghost's location (x,y): ({},{})".format(self.state.orange_ghost.x, self.state.orange_ghost.y))
            state = 'Frightened' if self.state.orange_ghost.state == LightState.FRIGHTENED else 'Normal'
            print('Orange ghost state: {}'.format(state))


def main():
    module = PacbotClient(SERVER_ADDRESS, SERVER_PORT)
    module.run()

if __name__ == "__main__":
    main()
