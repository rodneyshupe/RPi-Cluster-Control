#!/usr/bin/env python
"""This module is status RESTful API."""

from flask import Flask, jsonify
from flask_restful import Api
# Need to install the following modules:
# pip install flask flask_restful

from mod_status_info import StatusInfo

#Get Configuration
try:
    #Test for custom config
    import config_service_custom as CONFIG
except ImportError:
    #If custom config fails load default
    import config_service_default as CONFIG

app = Flask(__name__) # pylint: disable=invalid-name
api = Api(app) # pylint: disable=invalid-name

def do_shutdown(do_reboot=False):
    """ This function handles the Shutdown method of the API """

    if do_reboot:
        command = "(/bin/sleep 5s; sudo /sbin/shutdown -r now) &"
        action = "Reboot"
    else:
        command = "(/bin/sleep 5s; sudo /sbin/shutdown now) &"
        action = "Shutdown"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return {"action":action, "command":command, "result":output}

@app.route('/api/v1.0/status', methods=['GET'])
def api_status():
    """
    Get method returns status info in JSON.
    """
    return jsonify(StatusInfo().get_info()) # Fetches status info

@app.route('/api/v1.0/status/debug', methods=['GET'])
def api_status_debug():
    """ Get method returns status and debug info in JSON. """
    return jsonify(StatusInfo().get_info(True)) # Fetches status info

@app.route('/api/v1.0/debug', methods=['GET'])
def api_debug():
    """ Get method returns debug info in JSON. """
    return jsonify(StatusInfo().get_debug_info()) # Fetches status info

@app.route('/api/v1.0/shutdown', methods=['DELETE'])
def api_shutdown():
    """ Get method returns response to the shutdown shell command in JSON. """
    return jsonify(do_shutdown())

@app.route('/api/v1.0/shutdown/reboot', methods=['DELETE'])
def api_reboot():
    """ Get method returns response to the shutdown (with reboot) shell command in JSON. """
    return jsonify(do_shutdown(True))

if __name__ == '__main__':
    app.run(port=CONFIG.STATUS_API_PORT, host="0.0.0.0")
