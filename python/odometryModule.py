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

FREQUENCY = 40

LEFT_ENCODER = 29
RIGHT_ENCODER = 31

class OdometryModule(rm.ProtoModule):
    def __init__(self, addr, port):
        print("Initializing encoders...")
        self.subscriptions = [MsgType.ENCODER_CONTROL]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.initializeEncoders()
        self.leftClicks = 0
        self.rightClicks = 0
        self.running = False
        print("Encoders initialized")

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        if msg_type == MsgType.ENCODER_CONTROL:
            if msg.command == EncoderControl.BEGIN:
                self.begin()
            elif msg.command == EncoderControl.RESET:
                self.reset()

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        if self.running:
            msg = EncoderReport()
            msg.left = self.leftClicks
            msg.right = self.rightClicks
            msg = msg.SerializeToString()
            # print("Left Odometer: ", self.leftClicks)
            # print("Right Odometer: ", self.rightClicks)
            self.write(msg, MsgType.ENCODER_REPORT)

    def initializeEncoders(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(LEFT_ENCODER, GPIO.IN)
        GPIO.setup(RIGHT_ENCODER, GPIO.IN)

        time.sleep(1)

    def clickLeft(self, channel):
        if self.running:
            self.leftClicks += 1

    def clickRight(self, channel):
        if self.running:
            self.rightClicks += 1

    def begin(self):
        # GPIO.add_event_detect(LEFT_ENCODER, GPIO.BOTH, self.clickLeft)
        # GPIO.add_event_detect(RIGHT_ENCODER, GPIO.BOTH, self.clickRight)
        self.running = True

    def reset(self):
        print("Resetting odometers!")
        # if self.running:
        #     GPIO.remove_event_detect(LEFT_ENCODER)
        #     GPIO.remove_event_detect(RIGHT_ENCODER)
        self.running = False
        self.leftClicks = 0
        self.rightClicks = 0
        msg = EncoderReport()
        msg.left = self.leftClicks
        msg.right = self.rightClicks
        msg = msg.SerializeToString()

def destroy(*args):
    GPIO.cleanup()
    print("Odometry module safely terminated")
    sys.exit()

def main():
    signal.signal(signal.SIGINT, destroy)
    signal.signal(signal.SIGTERM, destroy)
    module = OdometryModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()