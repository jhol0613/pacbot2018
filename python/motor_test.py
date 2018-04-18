import RPi.GPIO as GPIO
import time

PWM_PIN = 32
CTRL_1 = 36
CTRL_2 = 38

FORWARD = 0
BACKWARD = 1

PWM = None

def setup():
	GPIO.setmode(GPIO.BOARD)

	IO.setup(CTRL_1, IO.OUT)
	IO.setup(CTRL_2, IO.OUT)
	GPIO.output(CTRL_1, False)
	GPIO.output(CTRL_2, False)

	IO.setup(PWM_PIN, IO.OUT)
	PWM = IO.PWM(PWM_PIN, 100)
	PWM.start(0)

	time.sleep(1) # wait for setup

def setDirection(direction):
	if direction == FORWARD:
		GPIO.output(CTRL_1, False)
		GPIO.output(CTRL_2, True)
	elif direction == BACKWARD:
		GPIO.output(CTRL_1, True)
		GPIO.output(CTRL_2, False)

def runMotor(duration, dutyCycle):
	startTime = time.time()
	PWM.changeDutyCycle(dutyCycle)
	while(time.time() - startTime < duration):
		pass
	PWM.changeDutyCycle(0)

def destroy():
	GPIO.output(CTRL_1, False)
	GPIO.output(CTRL_2, False)
	PWM.changeDutyCycle(0)
	GPIO.cleanup()


if __name__ == '__main__':     # Program start from here
  setup()
  try:
      setDirection(FORWARD)
	  runMotor(4, 40)
	  runMotor(4, 15)
	  time.sleep(1)
	  setDirection(BACKWARD)
	  runMotor(4, 40)
	  runMotor(4, 15)
  except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    destroy()



