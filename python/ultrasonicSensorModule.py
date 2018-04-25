#!/usr/bin/env python3

import os, random
import robomodules as rm
from messages import *

import RPi.GPIO as GPIO
import time
import signal
import sys

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11293)

FREQUENCY = 20

TIMEOUT_DISTANCE = 12 # Centimeters

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
        # start = time.time()
        msg = UltrasonicArray()
        msg.front_center = self.pulse(FRT_CTR)
        msg.front_left = self.pulse(FRT_LFT)
        msg.front_right = self.pulse(FRT_RGT)
        msg.rear_left = self.pulse(REAR_LFT)
        msg.rear_right = self.pulse(REAR_RGT)
        # end = time.time()
        # print("Measurement time: ", end-start)

        msg = msg.SerializeToString()
        self.write(msg, MsgType.ULTRASONIC_ARRAY)
        # end = time.time()
        # print("Tick time: ", end-start)

    def initializeSensors(self):
        GPIO.setmode(GPIO.BOARD)
        for pin in TRIG_PINS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
        for pin in ECHO_PINS:
            GPIO.setup(pin, GPIO.IN)
        time.sleep(1)

    def pulse(self, sensor):
        GPIO.output(TRIG_PINS[sensor], True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PINS[sensor], False)
        pulse_start = 0
        distance = TIMEOUT_DISTANCE

        while GPIO.input(ECHO_PINS[sensor])==0:
            pulse_start = time.time()
            distance = (time.time() - pulse_start) * 17150
            if distance > TIMEOUT_DISTANCE:
                return TIMEOUT_DISTANCE
        while GPIO.input(ECHO_PINS[sensor])==1:
            distance = (time.time() - pulse_start) * 17150
            if distance > TIMEOUT_DISTANCE:
                return TIMEOUT_DISTANCE

        distance = round(distance, 2)
        time.sleep(.001)
        return distance

    # Pulses 2 sensors at once to save time
    # def pulse2(self, sensor1, sensor2):
    #     GPIO.output(TRIG_PINS[sensor1], True)
    #     time.sleep(0.00001)
    #     GPIO.output(TRIG_PINS[sensor1], False)

    #     GPIO.output(TRIG_PINS[sensor2], True)
    #     time.sleep(0.00001)
    #     GPIO.output(TRIG_PINS[sensor2], False)

    #     while GPIO.input(ECHO_PINS[sensor])==0:
    #         pulse_start = time.time()
    #     while GPIO.input(ECHO_PINS[sensor])==1:
    #         distance = (time.time() - pulse_start) * 17150
    #         if distance > TIMEOUT_DISTANCE:
    #             return TIMEOUT_DISTANCE

    #     distance = round(distance, 2)
    #     return distance

def destroy(*args):
    GPIO.cleanup()
    print("Ultrasonic sensor module safely terminated")
    sys.exit()

def main():
    signal.signal(signal.SIGINT, destroy)
    signal.signal(signal.SIGTERM, destroy)
    module = UltrasonicSensorModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()