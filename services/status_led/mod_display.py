#!/usr/bin/env python

#
# To launch on boot, add the follwoing to the /etc/rc.local
# python /home/pi/StatusLED/display.py &
#

from time import sleep

from mod_state_file import state_file

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'lib'))
from lib_common import isnumeric

#Get Configuration
try:
    #Test for custom config
    import config_status_led_custom as CONFIG
except:
    #If custom config fails load default
    import config_status_led_default as CONFIG

class led_display():

    def __init__(self):
        self.RED_IDX = 0
        self.GREEN_IDX = 1
        self.BLUE_IDX = 2
        self.pins = [ CONFIG.RED_PIN, CONFIG.GREEN_PIN, CONFIG.BLUE_PIN ] # Red, Green, Blue
        self.pinstates = [ False, False, False ]
        self.blink_delay = CONFIG.BLINK_DELAY
        state_file().write(CONFIG.DEFAULT_DISPLAY_STATE)

    def _on(self, idx):
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.pins[idx], GPIO.OUT)
        GPIO.output(self.pins[idx], GPIO.HIGH)
        return (GPIO.input(self.pins[idx]) == GPIO.HIGH)

    def _off(self, idx):
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.pins[idx], GPIO.OUT)
        GPIO.output(self.pins[idx], GPIO.LOW)
        return (GPIO.input(self.pins[idx]) == GPIO.LOW)

    def on(self, idx):
        if idx < 0:
            raise IndexError("Index needs to be positive.")
        self.pinstates[idx] = True
        return(self._on(idx))

    def off(self, idx):
        if idx < 0:
            raise IndexError("Index needs to be positive.")
        self.pinstates[idx] = False
        return(self._off(idx))

    def toggle(self, idx):
        if self.pinstates[idx]:
            return(self.off(idx))
        else:
            return(self.on(idx))

    def set_blink_delay(self, delay):
        if isnumeric(delay) and delay >= 0:
            self.blink_delay = delay
            return(True)
        else:
            raise TypeError("Blink delay must be positive number. (" + str(delay) + ")")

    def setpin(self, idx, state):
        if idx < 0:
            raise IndexError("Index needs to be positive.")
        if isnumeric(state) and int(state) >= 0 and int(state) < 3:
            switcher = {
                0: self.off,
                1: self.on,
                2: self.toggle,
            }
            # Get the function from switcher dictionary
            func = switcher.get(int(state), lambda: "Invalid line number")
            # Execute the function
            return(func(idx))
        else:
            #print(state)
            #print(int(state) >= 0)
            #print(int(state) < 3)
            #print(int(state) == state)
            raise ValueError("Invalid Value: \"" + str(state) + "\" state must be between 0 and 2.")

    def setpins(self, states):
        if state_file().valid_state(states):
            red = self.setpin(self.RED_IDX, states[self.RED_IDX])
            green = self.setpin(self.GREEN_IDX, states[self.GREEN_IDX])
            blue = self.setpin(self.BLUE_IDX, states[self.BLUE_IDX])
            return(red and green and blue)
        else:
            raise ValueError("Invalid Value: \"" + str(states) + "\" state must be 3 digits in length.")

    def set_exit(self):
        return(state_file().write('exi'))

    def display(self):
        states = state_file().read()
        if states == "exi":
            return(False)
        return(self.setpins(states))
