#!/usr/bin/env python
""" Flask based API to handle the functionality of the Master Service API """

from functools import wraps
from flask import Flask, request, jsonify
from flask_restful import Api

from mod_master_control import MasterStatus, MasterLed

#Get Configuration
try:
    #Test for custom config
    import config_master_custom as CONFIG
except ImportError:
    #If custom config fails load default
    import config_master_default as CONFIG

app = Flask(__name__) # pylint: disable=invalid-name
api = Api(app) # pylint: disable=invalid-name
master_led_module = MasterLed() # pylint: disable=invalid-name

def check_auth(username, password):
    """
    Check Authentication
    """
    # TODO: Create a more robust authentication scheme
    return username == 'admin' and password == 'secret'

def authenticate():
    """
    Request Athentication
    """
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(function):
    '''
    Handle Authentication
    '''
    @wraps(function)
    def decorated(*args, **kwargs):
        '''
        Wrapper function
        '''
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return function(*args, **kwargs)

    return decorated

@app.errorhandler(404)
def not_found(error=None):
    '''
    Error 404 Not Found
    '''
    message = {
        'status': 404,
        'error': error,
        'message': "Not Found: " + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/api/v1.0/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    '''
    Echo Method just returns the calling protocal
    '''
    message = {"ECHO", request.method}
    return jsonify(message)

@app.route('/api/v1.0/nodes', methods=['GET'])
def api_nodes():
    '''
    Returns list of nodes
    '''
    return jsonify(MasterStatus().get_hosts())

@app.route('/api/v1.0/status', methods=['GET'])
def api_status():
    '''
    Fetches status info
    '''
    return jsonify(MasterStatus().get_status())

@app.route('/api/v1.0/status/debug', methods=['GET'])
def api_status_debug():
    '''
    Fetches status info with debug info
    '''
    return jsonify(MasterStatus().get_status(True))

@app.route('/api/v1.0/status/lines', methods=['GET'])
def api_status_lines():
    '''
    Fetches status info for one node
    '''
    return jsonify(MasterStatus().get_status_line())

@app.route('/api/v1.0//status/lines/<int:node>', methods=['GET'])
def api_status_lines_by_node(node):
    '''
    Fetches status info for one node
    '''
    return jsonify(MasterStatus().get_status_line(node=node))

@app.route('/api/v1.0//status/line/<line_type>', methods=['GET'])
def api_status_line(line_type):
    '''
    Fetches status info for one node
    '''
    return jsonify(MasterStatus().get_status_line(line_types=line_type))

@app.route('/api/v1.0//status/line/<line_type>/<int:node>', methods=['GET'])
def api_status_line_by_node(line_type, node):
    '''
    Fetches status info for one node
    '''
    return jsonify(MasterStatus().get_status_line(line_type, node))

@app.route('/api/v1.0/status/<int:node>', methods=['GET'])
def api_status_by_node(node):
    '''
    Fetches status info for one node
    '''
    return jsonify(MasterStatus().get_status(node))

@app.route('/api/v1.0/status/debug/<int:node>', methods=['GET'])
def api_debug_by_node(node):
    '''
    Fetches status info with debug info for one node
    '''
    return jsonify(MasterStatus().get_status(node), True)

@app.route('/api/v1.0/shutdown', methods=['DELETE'])
def api_shutdown():
    '''
    Shutdown all nodes
    '''
    return jsonify(MasterStatus().shutdown())

@app.route('/api/v1.0/shutdown/reboot', methods=['DELETE'])
def api_reboot():
    '''
    Reboot all nodes
    '''
    return jsonify(MasterStatus().reboot())

@app.route('/api/v1.0/shutdown/<int:node>', methods=['DELETE'])
def api_shutdown_node(node):
    '''
    Shutdown one node
    '''
    return jsonify(MasterStatus().shutdown(node))

@app.route('/api/v1.0/shutdown/reboot/<int:node>', methods=['DELETE'])
def api_reboot_node(node):
    '''
    Reboot one node
    '''
    return jsonify(MasterStatus().reboot(node))

@app.route('/api/v1.0/led', methods=['GET'])
def api_get_led():
    '''
    Get LED State for all nodes
    '''
    return jsonify(master_led_module.get_state())

@app.route('/api/v1.0/led/<node>', methods=['GET'])
def api_get_led_node(node):
    '''
    Get LED State by node
    '''
    return jsonify(master_led_module.get_state(node))

@app.route('/api/v1.0/led/<state>', methods=['PATCH'])
def api_set_led(state):
    '''
    Set LED State
    '''
    return jsonify(master_led_module.set_state(state))

@app.route('/api/v1.0/led/<node>/<state>', methods=['PATCH'])
def api_set_led_state(node, state):
    '''
    Set LED State by node.
    '''
    return jsonify(master_led_module.set_state(state, node))

@app.route('/api/v1.0/led/mode/<mode>', methods=['PATCH'])
def api_set_led_mode(mode):
    '''
    Get LED State mode.
    '''
    return jsonify(master_led_module.set_mode(mode))

@app.route('/api/v1.0/led/pattern/<pattern>', methods=['PATCH'])
def api_set_led_pattern(pattern):
    '''
    Get LED Pattern
    '''
    return jsonify(master_led_module.set_pattern(pattern))

@app.route('/api/v1.0/led/pattern/<pattern>/<int:speed>', methods=['PATCH'])
def api_set_led_pattern_speed(pattern, speed):
    '''
    Set LED patern and speed
    '''
    return jsonify(master_led_module.set_pattern(pattern, speed))

if __name__ == '__main__':
    app.debug = CONFIG.APP_DEBUG
    app.run(port=CONFIG.MASTER_API_PORT, host="0.0.0.0")
