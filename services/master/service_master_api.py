#!/usr/bin/env python

from mod_master_control import master_status, master_led

from flask import Flask, request, jsonify, json
from flask_restful import Resource, Api
"""
Need to install the following modules:
pip install flask flask_restful
"""

#Get Configuration
try:
    #Test for custom config
    import config_master_custom as CONFIG
except:
    #If custom config fails load default
    import config_master_default as CONFIG

app = Flask(__name__)
api = Api(app)
master_led_module = master_led()
class nodes(Resource):
    def get(self):
        return(jsonify(master_status().get_hosts())) # Displays list of nodes

class status(Resource):
    def get(self):
        return(jsonify(master_status().get_status())) # Fetches status info

class status_debug(Resource):
    def get(self):
        return(jsonify(master_status().get_status(True))) # Fetches status info with debug info

class status_lines(Resource):
    def get(self):
        return(jsonify(master_status().get_status_line())) # Fetches status info for one node

class status_lines_by_node(Resource):
    def get(self, node):
        return(jsonify(master_status().get_status_line(node = node))) # Fetches status info for one node

class status_line(Resource):
    def get(self, line_type):
        return(jsonify(master_status().get_status_line(line_type = line_type))) # Fetches status info for one node

class status_line_by_node(Resource):
    def get(self, line_type, node):
        return(jsonify(master_status().get_status_line(line_type, node))) # Fetches status info for one node

class status_by_node(Resource):
    def get(self, node):
        return(jsonify(master_status().get_status(node))) # Fetches status info for one node

class debug_by_node(Resource):
    def get(self, node):
        return(jsonify(master_status().get_status(node), True)) # Fetches status info with debug info for one node

class shutdown(Resource):
    def get(self):
        return(jsonify(master_status().shutdown())) # Shutdown all nodes

class reboot(Resource):
    def get(self):
        return(jsonify(master_status().reboot())) # Reboot all nodes

class shutdown_node(Resource):
    def get(self, node):
        return(jsonify(master_status().shutdown(node))) # Shutdown one node

class reboot_node(Resource):
    def get(self, node):
        return(jsonify(master_status().reboot(node))) # Reboot one node

class get_led(Resource):
    def get(self):
        return(jsonify(master_led_module.get_state())) # Get LED State for all nodes

class get_led_node(Resource):
    def get(self, node):
        return(jsonify(master_led_module.get_state(node))) # Get LED State by node.

class set_led(Resource):
    def get(self, state):
        return(jsonify(master_led_module.set_state(state))) # Get LED State for all nodes

class set_led_node(Resource):
    def get(self, state, node):
        return(jsonify(master_led_module.set_state(state, node))) # Get LED State by node.

class set_led_mode(Resource):
    def get(self, mode):
        return(jsonify(master_led_module.set_mode(mode))) # Get LED State by node.

class set_led_pattern(Resource):
    def get(self, pattern):
        return(jsonify(master_led_module.set_pattern(pattern))) # Get LED State by node.

class set_led_pattern_speed(Resource):
    def get(self, pattern, speed):
        return(jsonify(master_led_module.set_pattern(pattern,speed))) # Get LED State by node.

api.add_resource(nodes, '/api/v1.0/nodes')
api.add_resource(status, '/api/v1.0/status')
api.add_resource(status_debug, '/api/v1.0/status/debug')
api.add_resource(status_lines, '/api/v1.0/status/lines')
api.add_resource(status_lines_by_node, '/api/v1.0//status/lines/<node>')
api.add_resource(status_line, '/api/v1.0//status/line/<line_type>')
api.add_resource(status_line_by_node, '/api/v1.0//status/line/<line_type>/<node>')
api.add_resource(status_by_node, '/api/v1.0/status/<node>')
api.add_resource(debug_by_node, '/api/v1.0/status/debug/<node>')
api.add_resource(shutdown, '/api/v1.0/shutdown')
api.add_resource(reboot, '/api/v1.0/shutdown/reboot')
api.add_resource(shutdown_node, '/api/v1.0/shutdown/<node>')
api.add_resource(reboot_node, '/api/v1.0/shutdown/reboot/<node>')
api.add_resource(get_led, '/api/v1.0/get_led')
api.add_resource(get_led_node, '/api/v1.0/get_led/<node>')
api.add_resource(set_led, '/api/v1.0/set_led/<state>')
api.add_resource(set_led_mode, '/api/v1.0/set_led/mode/<mode>')
api.add_resource(set_led_pattern, '/api/v1.0/set_led/pattern/<pattern>')
api.add_resource(set_led_pattern_speed, '/api/v1.0/set_led/pattern/<pattern>/<speed>')

if __name__ == '__main__':
     app.run(port=CONFIG.MASTER_API_PORT, host="0.0.0.0")
