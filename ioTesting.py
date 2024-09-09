import RPi.GPIO as GPIO
import time


shutterPin = 18 #24
focusPin = 16 #23

GPIO.setmode(GPIO.BOARD)
GPIO.setup(shutterPin, GPIO.OUT)
GPIO.setup(focusPin,GPIO.OUT)
print("Setup done")

for x in range(0, 10):
	print("On")
	GPIO.output(focusPin, GPIO.HIGH)
	time.sleep(1)
	print("Off")
	GPIO.output(focusPin,GPIO.LOW)
	time.sleep(1)

GPIO.cleanup()
