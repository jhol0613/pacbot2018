#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *

import RPi.GPIO as GPIO
import time
import atexit

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11293)

FREQUENCY = 30

LEFT_BUTTON = 3
RIGHT_BUTTON = 5

class BumperModule(rm.ProtoModule):
    def __init__(self, addr, port):
        print("Initializing Bumpers...")
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
        self.initializeSensors()
        self.leftFlag = False;
        self.rightFlag = False;
        self.leftSent = False;
        self.rightSent = False;
        print("Bumpers Initialized")

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        return

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        msg = Bumper()
        
        if not self.leftSent:
            if self.leftFlag:
                msg.side = Bumper.LEFT
                msg = msg.SerializeToString()
                self.write(msg, MsgType.Bumper)
                self.leftSent = True
        else:
            if not self.leftFlag:
                self.leftSent = False

        if not self.rightSent:
            if self.rightFlag:
                msg.side = Bumper.RIGHT
                msg = msg.SerializeToString()
                self.write(msg, MsgType.Bumper)
                self.rightSent = True
        else:
            if not self.rightFlag:
                self.rightSent = False

    def initializeBumpers(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(LEFT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RIGHT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(LEFT_BUTTON, GPIO.BOTH, lambda _: self.leftFlag = not self.leftFlag, bouncetime=300)
        GPIO.add_event_detect(RIGHT_BUTTON, GPIO.BOTH, lambda _: self.rightFlag = not self.rightFlag, bouncetime=300)

        time.sleep(1)


def destroy():
    GPIO.cleanup()
    print("Program safely terminated")

def main():
    atexit.register(destroy)
    module = BumperModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()