#!/usr/bin/env python

#
# To launch on boot, add the follwoing to the /etc/rc.local
# python /home/pi/StatusLED/display.py &
#

from time import sleep

from mod_state_file import state_file
from mod_display import led_display

def main(led_display_module = led_display()):
    # Set the inital state to Blinking Green
    while led_display_module.display():
        sleep(led_display_module.blink_delay)

main()
