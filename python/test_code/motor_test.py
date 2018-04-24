import RPi.GPIO as IO
import time

PWM_PIN = 32
CTRL_1 = 36
CTRL_2 = 38

ENCODER = 29

FORWARD = 0
BACKWARD = 1

encoder_count = 0

def encoderCallback(channel):
	global encoder_count
	print("got here")
	encoder_count += 1

def setup():
	IO.setmode(IO.BOARD)

	IO.setup(CTRL_1, IO.OUT)
	IO.setup(CTRL_2, IO.OUT)
	IO.output(CTRL_1, False)
	IO.output(CTRL_2, False)

	IO.setup(ENCODER, IO.IN)
	IO.add_event_detect(ENCODER, IO.BOTH, encoderCallback)

	IO.setup(PWM_PIN, IO.OUT)
	global PWM
	PWM = IO.PWM(PWM_PIN, 100)
	PWM.start(0)

	global encoder_count
	encoder_count = 0

	time.sleep(1) # wait for setup

def setDirection(direction):
	if direction == FORWARD:
		IO.output(CTRL_1, False)
		IO.output(CTRL_2, True)
	elif direction == BACKWARD:
		IO.output(CTRL_1, True)
		IO.output(CTRL_2, False)

def runMotor(duration, dutyCycle):
	startTime = time.time()
	PWM.ChangeDutyCycle(dutyCycle)
	while(time.time() - startTime < duration):
		#print(IO.input(ENCODER))
		pass
	PWM.ChangeDutyCycle(0)

def destroy():
	IO.output(CTRL_1, False)
	IO.output(CTRL_2, False)
	PWM.ChangeDutyCycle(0)
	IO.cleanup()


if __name__ == '__main__':     # Program start from here
	setup()
	try:
		setDirection(FORWARD)
		runMotor(4, 100)
		print("Encoder Count: ", encoder_count)
		runMotor(4, 50)
		print("Encoder Count: ", encoder_count)
		time.sleep(1)
		setDirection(BACKWARD)
		runMotor(4, 100)
		print("Encoder Count: ", encoder_count)
		runMotor(4, 50)
		print("Encoder Count: ", encoder_count)
		destroy()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()



