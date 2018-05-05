#!/usr/bin/env python
'''
Class Method for handling the State File.
'''

import os
import re

class StateFile():
    '''
    Methods for manipulating State File.
    '''
    def __init__(self):
        # Get the path to the state file.
        # not sure if their is a better way but this works
        self.state_file_path = os.path.dirname(os.path.realpath(__file__))
        self.state_file_path += "/.state"

    @classmethod
    def valid_state(cls, states):
        '''
        Check if state is valid
        '''
        return re.match(re.compile("^[0-2][0-2][0-2]$"), str(states)) or states == 'exi'

    def state_file(self):
        '''
        Return State File Path
        '''
        return self.state_file_path

    def init(self, states="000"):
        '''
        Initialize State File
        '''
        self.write(states)
        return states

    def read(self):
        '''
        Read State from File
        '''
        try:
            file = open(self.state_file_path, "r")
            states = file.read(3)
            file.close()
        except:
            raise IOError("Error reading state file: " + self.state_file_path)

        return states

    def write(self, states):
        '''
        Write State to State File
        '''
        if not self.valid_state(states):
            raise ValueError("Invalid Value: \"" + states + "\" State must be 3 digits.")

        try:
            file = open(self.state_file_path, "w")
            file.write(states)
            file.close()
        except:
            raise IOError("Error writing state file: " + self.state_file_path)

        return states
