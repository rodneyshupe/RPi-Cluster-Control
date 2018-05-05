#!/usr/bin/env python

"""
Need to install the following modules:
pip install flask flask_restful
"""

from flask import Flask, jsonify
from flask_restful import Api

from mod_state_file import StateFile

#Get Configuration
try:
    #Test for custom config
    import config_status_led_custom as CONFIG
except ImportError:
    #If custom config fails load default
    import config_status_led_default as CONFIG

app = Flask(__name__) # pylint: disable=invalid-name
api = Api(app) # pylint: disable=invalid-name


@app.route('/api/v1.0/state', methods=['GET']) # Route_1
def api_get_state():
    """
    No input paramters
    Returns current state
    """
    return jsonify({"state":StateFile().read()})

@app.route('/api/v1.0/state/<state>', methods=['PATCH']) # Route_2
def api_set_state(state):
    """
    Takes desired state as paramter
    Returns resulting state in JSON
    """
    try:
        response = {'state': StateFile().write(state)}
    except IOError as exception:
        response = {
            'state': StateFile().read(),
            'error': "I/O error(" + exception.errno + "): " + exception.strerror
        }
    except ValueError as value_error:
        response = {
            'state': StateFile().read(),
            'error': str(value_error)
        }
    return jsonify(response)

if __name__ == '__main__':
    app.debug = CONFIG.APP_DEBUG
    app.run(port=CONFIG.PORT, host="0.0.0.0")
