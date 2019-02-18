__author__ = 'Ohad Shai'
__project__ = 'kookoo'

import os
import sys
from flask import Flask, request, Response

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)


from common.SettingsHandler import SettingsHandler
from server.functions_handler import FunctionsHandler
from server.server_logger import log

functions_handler = FunctionsHandler()

app = Flask(__name__)


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERT_DIR = os.path.join(os.path.join(ROOT_DIR, 'common'), 'cert')
SETTINGS_PATH = os.path.join(ROOT_DIR, 'settings.ini')


@app.route('/GetFunction', methods=['GET'])
def get_function():
    try:
        function_name = functions_handler.get_random_function()
        if not function_name:
            log.info("No Functions in File")
            return Response(status=200)
    except Exception as e:
        log.error("Internal Error ! Reason : {}".format(e))
        response = Response(response="Internal Server Error", status=500)
    else:
        log.info("Sending function name '{}' to Client".format(function_name))
        response = Response(response=function_name, status=200)

    return response


@app.route('/SendResponse', methods=['POST'])
def response_function():
    try:
        function_response = request.get_data()
        if function_response:
            log.info(function_response)
    except Exception:
        response = Response(response="Internal Server Error", status=500)
    else:
        response = Response("Server Received response function successfully", status=200)

    return response

if __name__ == '__main__':
    functions_handler.get_functions_from_file()
    settings_handler = SettingsHandler()
    ip, port = settings_handler.get_setting("Server", "ip"), settings_handler.get_setting("Server", "port")
    log.info("**** Starting HTTP Server ****")
    app.run(host=ip, port=port, ssl_context=(
        os.path.join(CERT_DIR, 'cert.pem'), os.path.join(CERT_DIR, 'key.pem')))
