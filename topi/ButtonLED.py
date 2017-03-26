#!/usr/bin/env python
########################################################################
# Filename    : ButtonLED.py
# Description : Controlling an led by button.
# Author      : freenove
# modification: 2016/06/12
########################################################################
import RPi.GPIO as GPIO
import time


buttonPin = 11    # define the buttonPin

def setup():
	print("Program is started")
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set buttonPin's mode is input, and pull up to high level(3.3V)

def loop():
	while True:
		if GPIO.input(buttonPin)==GPIO.LOW:
			print("Button pressed")
		else :
			print("Botton nor preesed")
	time.sleep(0.2)			

def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

