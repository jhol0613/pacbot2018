#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *

import RPi.GPIO as GPIO
import time
import signal
import sys

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11293)

FREQUENCY = 30

LEFT_BUTTON = 3
RIGHT_BUTTON = 5

class BumperModule(rm.ProtoModule):
    def __init__(self, addr, port):
        print("Initializing Bumpers...")
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
        self.initializeBumpers()
        self.leftFlag = False;
        self.rightFlag = False;
        # self.leftSent = False;
        # self.rightSent = False;
        print("Bumpers Initialized")

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        return

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        msg = Bumper()
        
        # if not self.leftSent:
        #     if self.leftFlag:
        #         msg.side = Bumper.LEFT
        #         self.write(msg.SerializeToString(), MsgType.BUMPER)
        #         self.leftSent = True
        # else:
        #     if not self.leftFlag:
        #         self.leftSent = False

        # if not self.rightSent:
        #     if self.rightFlag:
        #         msg.side = Bumper.RIGHT
        #         self.write(msg.SerializeToString(), MsgType.BUMPER)
        #         self.rightSent = True
        # else:
        #     if not self.rightFlag:
        #         self.rightSent = False

        if self.leftFlag:
            msg.side = Bumper.LEFT
            self.write(msg.SerializeToString(), MsgType.BUMPER)
            self.leftFlag = False
        
        if self.rightFlag:
            msg.side = Bumper.RIGHT
            self.write(msg.SerializeToString(), MsgType.BUMPER)
            self.rightFlag = False


    def setLeftFlag(self, channel):
        self.leftFlag = True

    def setRightFlag(self, channel):
        self.rightFlag = True

    def initializeBumpers(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(LEFT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RIGHT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(LEFT_BUTTON, GPIO.FALLING, self.setLeftFlag, bouncetime=300)
        GPIO.add_event_detect(RIGHT_BUTTON, GPIO.FALLING, self.setRightFlag, bouncetime=300)

        time.sleep(1)


def destroy(*args):
    GPIO.cleanup()
    print("Bumper module safely terminated")
    sys.exit()

def main():
    signal.signal(signal.SIGINT, destroy)
    signal.signal(signal.SIGTERM, destroy)
    module = BumperModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()