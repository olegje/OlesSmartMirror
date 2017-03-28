#!/usr/bin/env python
########################################################################
# Filename    : Mirrorbuttons.py
# Description : Controlling the buttons in the mirror frame
# Author      : Gjengedal
# modification: 28.03.2017
########################################################################
import time
import RPi.GPIO as GPIO
class ButtonControll():
    def __init__(self):
        self.buttonPins = [11, 13, 15]
        self.button_states = [False, False, False]
        self.setup()
    def setup(self):
        print("program is starting")
        GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location
        for pin in self.buttonPins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #configure pins and pull up resistor

    def loop(self):
        while True:
            for pin in self.buttonPins:
                if GPIO.input(pin) == GPIO.LOW:
                    print("Pin% is preesed" %pin)
                    self.button_states = [False, False, False]
                    if pin == 11:
                        self.button_states[0] = True
                    elif pin == 13:
                        self.button_states[1] = True
                    else:
                        self.button_states[2] = True
                else:
                    pass
            time.sleep(0.2)
    def destroy(self):
        GPIO.cleanup()

if __name__ == '__main__':
    buttonControll = ButtonControll()
    try:
        buttonControll.loop()
    except KeyboardInterrupt:
        buttonControll.destroy()






