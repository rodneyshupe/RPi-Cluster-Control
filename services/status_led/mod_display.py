#!/usr/bin/env python
'''
To launch on boot, add the follwoing to the /etc/rc.local
python /home/pi/StatusLED/display.py &
'''

import os
import sys

from mod_state_file import StateFile

# pylint: disable=wrong-import-position
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'lib'))
from lib_common import isnumeric
# pylint: enable=wrong-import-position

#Get Configuration
try:
    #Test for custom config
    import config_status_led_custom as CONFIG
except ImportError:
    #If custom config fails load default
    import config_status_led_default as CONFIG

class LedDisplay():
    '''
    Methods to controll GPIO Led
    '''

    def __init__(self):
        self.red_idx = 0
        self.green_idx = 1
        self.blue_idx = 2
        self.pins = [CONFIG.RED_PIN, CONFIG.GREEN_PIN, CONFIG.BLUE_PIN] # Red, Green, Blue
        self.pinstates = [False, False, False]
        self.blink_delay = CONFIG.BLINK_DELAY
        StateFile().write(CONFIG.DEFAULT_DISPLAY_STATE)

    def _on(self, idx):
        import RPi.GPIO as GPIO # pylint: disable=E0401
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.pins[idx], GPIO.OUT)
        GPIO.output(self.pins[idx], GPIO.HIGH)

        return GPIO.input(self.pins[idx]) == GPIO.HIGH

    def _off(self, idx):
        import RPi.GPIO as GPIO # pylint: disable=E0401
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.pins[idx], GPIO.OUT)
        GPIO.output(self.pins[idx], GPIO.LOW)

        return GPIO.input(self.pins[idx]) == GPIO.LOW

    def on(self, idx):  # pylint: disable=C0103
        '''
        Turn on LED pin.
        '''
        if idx < 0:
            raise IndexError("Index needs to be positive.")

        self.pinstates[idx] = True

        return self._on(idx)

    def off(self, idx):
        '''
        Turn off LED pin.
        '''
        if idx < 0:
            raise IndexError("Index needs to be positive.")

        self.pinstates[idx] = False

        return self._off(idx)

    def toggle(self, idx):
        '''
        Toggle on LED pin.
        '''
        if self.pinstates[idx]:
            value = self.off(idx)
        else:
            value = self.on(idx)

        return value

    def set_blink_delay(self, delay):
        '''
        Set blink_delay
        '''
        if isnumeric(delay) and delay >= 0:
            self.blink_delay = delay
            return True
        else:
            raise TypeError("Blink delay must be positive number. (" + str(delay) + ")")

    def setpin(self, idx, state):
        '''
        Set pin based on state
        '''
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
            return func(idx)
        else:
            #print(state)
            #print(int(state) >= 0)
            #print(int(state) < 3)
            #print(int(state) == state)
            error_msg = "Invalid Value: \"" + str(state) + "\" state must be between 0 and 2."
            raise ValueError(error_msg)


    def setpins(self, states):
        '''
        Set all pins acording to state
        '''
        if StateFile().valid_state(states):
            red = self.setpin(self.red_idx, states[self.red_idx])
            green = self.setpin(self.green_idx, states[self.green_idx])
            blue = self.setpin(self.blue_idx, states[self.blue_idx])
            return red and green and blue
        else:
            error_msg = "Invalid Value: \"" + str(states) + "\" state must be 3 digits in length."
            raise ValueError(error_msg)

    @classmethod
    def set_exit(cls):
        '''
        Set state value to indicate exit
        '''
        return StateFile().write('exi')

    def display(self):
        '''
        Read state and set pins if not ready to exit
        '''
        states = StateFile().read()
        if states == "exi":
            return_value = False
        else:
            return_value = self.setpins(states)
        return return_value
