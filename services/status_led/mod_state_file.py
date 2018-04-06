#!/usr/bin/env python

import os
import re

class state_file():
    def __init__(self):
        # Get the path to the state file.
        # not sure if their is a better way but this works
        self.state_file_path = os.path.dirname(os.path.realpath(__file__))
        self.state_file_path += "/.state"

    def valid_state(self, states):
        return(re.match(re.compile("^[0-2][0-2][0-2]$"), str(states)) or states == 'exi')

    def state_file(self):
        return(self.state_file_path)

    def init(self, states = "000"):
        self.write(states)
        return(states)

    def read(self):
        try:
            file = open(self.state_file_path, "r")
            states = file.read(3)
            file.close()
        except:
            raise IOError("Error reading state file: " + self.state_file_path)

        return(states)

    def write(self, states):
        import re

        if not self.valid_state(states):
            raise ValueError("Invalid Value: \"" + states + "\" State must be 3 digits.")

        try:
            file = open(self.state_file_path, "w")
            file.write(states)
            file.close()
        except:
            raise IOError("Error writing state file: " + self.state_file_path)

        return(states)
