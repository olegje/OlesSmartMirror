#!/usr/bin/env python
########################################################################
# Filename    : Mirrorbuttons.py
# Description : Controlling the buttons in the mirror frame
# Author      : Gjengedal
# modification: 04.04.2017
########################################################################
import RPi.GPIO as GPIO
class ButtonControll():
    def __init__(self):
        self.buttonPins = [11, 13, 15]
        self.button_states = [False, False, False]
        self.setup()
    def setup(self):
        print("ButtonControll started")
        GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location
        for pin in self.buttonPins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #configure pins and pull up resistor
    def destroy(self):
        GPIO.cleanup()

if __name__ == '__main__':
    buttonControll = ButtonControll()
    try:
        buttonControll.check_buttons()
    except KeyboardInterrupt:
        buttonControll.destroy()






