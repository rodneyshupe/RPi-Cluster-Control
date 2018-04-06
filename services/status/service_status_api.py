#!/usr/bin/env python

from mod_status_info import status_info

from flask import Flask, request, jsonify, json
from flask_restful import Resource, Api
"""
Need to install the following modules:
pip install flask flask_restful
"""

#Get Configuration
try:
    #Test for custom config
    import config_service_custom as CONFIG
except:
    #If custom config fails load default
    import config_service_default as CONFIG

app = Flask(__name__)
api = Api(app)

def do_shutdown(reboot = False):
    if reboot:
        command = "/usr/bin/sudo /sbin/shutdown -r now"
        action = "Reboot"
    else:
        command = "/usr/bin/sudo /sbin/shutdown now"
        action = "Shutdown"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return( {"action":action, "command":command, "result":output} )

class status(Resource):
    def get(self):
        return(jsonify(status_info().get_info())) # Fetches status info

class status_debug(Resource):
    def get(self):
        return(jsonify(status_info().get_info(True))) # Fetches status info

class debug(Resource):
    def get(self):
        return(jsonify(status_info().get_debug_info())) # Fetches status info

class shutdown(Resource):
    def get(self):
        return(jsonify(do_shutdown()))

class reboot(Resource):
    def get(self):
        return(jsonify(do_shutdown(True)))

api.add_resource(status, '/api/v1.0/status')
api.add_resource(status_debug, '/api/v1.0/status/debug')
api.add_resource(debug, '/api/v1.0/debug')
api.add_resource(shutdown, '/api/v1.0/shutdown')
api.add_resource(reboot, '/api/v1.0/shutdown/reboot')

if __name__ == '__main__':
     app.run(port=CONFIG.STATUS_API_PORT, host="0.0.0.0")
