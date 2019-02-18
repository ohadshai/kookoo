__author__ = 'Ohad Shai'
__project__ = 'kookoo'

import os
import sys
from flask import Flask, request, Response

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERT_DIR = os.path.join(os.path.join(ROOT_DIR, 'common'), 'cert')
sys.path.append(ROOT_DIR)

from common.SettingsHandler import SettingsHandler
from server.functions_handler import FunctionsHandler
from server.server_logger import log

app = Flask(__name__)
functions_handler = FunctionsHandler()


@app.route('/GetFunction', methods=['GET'])
def get_function():
    """
    Server send a randomize function name
    :return:
    """
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
def send_response():
    """
    Server handles response after executing function
    :return:
    """
    try:
        function_response = request.get_data() if sys.version_info[0] < 3 else request.get_data().decode()
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
