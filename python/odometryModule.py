#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *

import RPi.GPIO as GPIO
import time
import signal

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11293)

FREQUENCY = 30

LEFT_ENCODER = 29
RIGHT_ENCODER = 31

class OdometryModule(rm.ProtoModule):
    def __init__(self, addr, port):
        print("Initializing encoders...")
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
        self.initializeEncoders()
        self.leftClicks = 0
        self.rightClicks = 0
        self.running = False
        print("Encoders initialized")

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        if msg_type == MsgType.EncoderControl:
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
            self.write(msg, MsgType.EncoderReport)

    def initializeBumpers(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(LEFT_ENCODER, GPIO.IN)
        GPIO.setup(RIGHT_ENCODER, GPIO.IN)

        time.sleep(1)

    def begin(self):
        GPIO.add_event_detect(LEFT_ENCODER, GPIO.RISING, lambda _: self.leftClicks += 1)
        GPIO.add_event_detect(RIGHT_ENCODER, GPIO.RISING, lambda _: self.rightClicks += 1)
        self.running = True

    def reset(self):
        if self.running:
            GPIO.remove_event_detect(LEFT_ENCODER)
            GPIO.remove_event_detect(RIGHT_ENCODER)
        self.running = False
        self.leftClicks = 0
        self.rightClicks = 0

def destroy():
    GPIO.cleanup()
    print("Odometry module safely terminated")

def main():
    signal.signal(signal.SIGINT, destroy)
    signal.signal(signal.SIGTERM, destroy)
    module = BumperModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()