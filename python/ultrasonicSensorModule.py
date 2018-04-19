#!/usr/bin/env python3

import os, random
import robomodules as rm
from messages import *

import RPi.GPIO as GPIO
import time

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 10

TRIG_PINS = [7, 11, 15, 21, 23]
ECHO_PINS = [8, 12, 16, 22, 24]

# Indices for accessing trigger and echo pins
FRT_CTR = 0
FRT_LFT = 1
FRT_RGT = 2
REAR_LFT = 3
REAR_RGT = 4

class UltrasonicSensorModule(rm.ProtoModule):
    def __init__(self, addr, port):
        print("Initializing Ultrasonic Sensors...")
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
        self.initializeSensors()
        print("Ultrasonic Sensors Initialized")

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        return

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        msg = UltrasonicArray()
        msg.front_center = self.pulse(FRT_CTR)
        msg.front_left = self.pulse(FRT_LFT)
        msg.front_right = self.pulse(FRT_RGT)
        msg.rear_left = self.pulse(REAR_LFT)
        msg.rear_right = self.pulse(REAR_RGT)

        msg = msg.SerializeToString()
        self.write(msg, MsgType.UltrasonicArray)

    def initializeSensors(self):
        for pin in TRIG_PINS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
        for pin in ECHO_PINS:
            GPIO.setup(pin, GPIO.IN)
        time.sleep(2)

    def pulse(self, sensor):
        GPIO.output(TRIG_PINS[sensor], True)
        time.sleep(0.00001)
        GPIO.output(sensor, False)
        while GPIO.input(ECHO_PINS[sensor])==0:
            pulse_start = time.time()
        while GPIO.input(ECHO_PINS[sensor])==1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return distance

def main():
    module = UltrasonicSensorModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()