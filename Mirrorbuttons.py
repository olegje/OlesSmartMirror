#!/usr/bin/env python
########################################################################
# Filename    : Mirrorbuttons.py
# Description : Controlling the buttons in the mirror frame
# Author      : Gjengedal
# modification: 02.04.2017
########################################################################
import time
import RPi.GPIO as GPIO
import pprint
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

    def loop(self, app):
        while True:
            print("while")
            print(app.state)
            for pin in self.buttonPins:
                if GPIO.input(pin) == GPIO.LOW:
                    print("Pin% is preesed" %pin)
                    if pin == 11:
                        self.button_states[0] = True
                        app.show_frame(PageOne)
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






