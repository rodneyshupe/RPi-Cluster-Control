#!/usr/bin/env python
'''
To launch on boot, add the follwoing to the /etc/rc.local
python /home/pi/StatusLED/display.py &
'''

from time import sleep

from mod_display import LedDisplay

def main(led_display_module=LedDisplay()):
    '''
    Set the inital state to Blinking Green
    '''
    while led_display_module.display():
        sleep(led_display_module.blink_delay)

main()
