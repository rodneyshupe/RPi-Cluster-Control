#!/usr/bin/env python

from flask import Flask, request, jsonify, json
from flask_restful import Resource, Api

"""
Need to install the following modules:
pip install flask flask_restful
"""
from mod_state_file import state_file

#Get Configuration
try:
    #Test for custom config
    import config_status_led_custom as CONFIG
except:
    #If custom config fails load default
    import config_status_led_default as CONFIG

app = Flask(__name__)
api = Api(app)

class get_state(Resource):
    def get(self):
        return(jsonify( { "state":state_file().read() } ))

class set_state(Resource):
    def get(self, state):
        try:
            response = { 'state': state_file().write(state) }
        except Exception as e:
            response = { 'state': state_file().read(), 'error':str(e) }
        return(jsonify( response ))

api.add_resource(get_state, '/api/v1.0/state') # Route_1
api.add_resource(set_state, '/api/v1.0/state/<state>') # Route_2

if __name__ == '__main__':
     app.run(port=CONFIG.PORT, host="0.0.0.0")
