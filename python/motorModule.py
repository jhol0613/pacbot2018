#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *

import RPi.GPIO as GPIO
import time
import atexit
import signal

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11293)

FREQUENCY = 0

LEFT_PWM = 32
LEFT_1 = 36
LEFT_2 = 38
RIGHT_PWM = 33
RIGHT_1 = 35
RIGHT_2 = 37

BACKWARD = 0
FORWARD = 1

LEFT_MOTOR = 0
RIGHT_MOTOR = 1

class MotorModule(rm.ProtoModule):
    def __init__(self, addr, port):
        print("Initializing Motors...")
        self.subscriptions = [MsgType.TWIST]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.initializeMotors()
        self.leftSpeed = 0
        self.rightSpeed = 0
        self.leftDir = 0
        self.rightDir = 0
        print("Motors Initialized")

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        if msg_type == MsgType.TWIST:
            self.processTwist(msg.velocity, msg.omega)

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        print("tick")
        return

    def initializeMotors(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(LEFT_PWM, GPIO.OUT)
        GPIO.setup(LEFT_1, GPIO.OUT)
        GPIO.setup(LEFT_2, GPIO.OUT)
        GPIO.setup(RIGHT_PWM, GPIO.OUT)
        GPIO.setup(RIGHT_1, GPIO.OUT)
        GPIO.setup(RIGHT_2, GPIO.OUT)

        self.right_pwm = GPIO.PWM(RIGHT_PWM, 100)
        self.left_pwm = GPIO.PWM(LEFT_PWM, 100)

        self.right_pwm.start(0)
        self.left_pwm.start(0)
        self.setDirection(LEFT_MOTOR, FORWARD)
        self.setDirection(RIGHT_MOTOR, FORWARD)

        time.sleep(1)

    def setDirection(self, motor, direction):
        if motor == LEFT_MOTOR:
            if direction == FORWARD:
                GPIO.output(LEFT_1, True)
                GPIO.output(LEFT_2, False)
            else:
                GPIO.output(LEFT_1, False)
                GPIO.output(LEFT_2, True)
        else:
            if direction == FORWARD:
                GPIO.output(RIGHT_1, True)
                GPIO.output(RIGHT_2, False)
            else:
                GPIO.output(RIGHT_1, False)
                GPIO.output(RIGHT_2, True)

    # Takes linear and rotational values and converts into signals for left and right motor
    def processTwist(self, linSpeed, rotSpeed):
        leftSpeed = linSpeed
        rightSpeed = linSpeed

        leftSpeed += rotSpeed
        rightSpeed -= rotSpeed

        if leftSpeed > 100 or leftSpeed < -100 or rightSpeed > 100 or rightSpeed < -100:
            print("Exceeded speed limits!")
        else:
            if leftSpeed >= 0:
                self.setDirection(LEFT_MOTOR, FORWARD)
            else:
                self.setDirection(LEFT_MOTOR, BACKWARD)
            if rightSpeed >= 0:
                self.setDirection(RIGHT_MOTOR, FORWARD)
            else:
                self.setDirection(RIGHT_MOTOR, BACKWARD)
            print("Left speed: ", leftSpeed)
            print("Right speed: ", rightSpeed)
            self.left_pwm.ChangeDutyCycle(abs(leftSpeed))
            self.right_pwm.ChangeDutyCycle(abs(rightSpeed))

def destroy():
    GPIO.cleanup()
    print("Cleaned up motor pins")
    print("Program safely terminated")

def main():
    #atexit.register(destroy)
    signal.signal(signal.SIGINT, destroy)
    signal.signal(signal.SIGTERM, destroy)
    module = MotorModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()