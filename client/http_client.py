__author__ = 'Ohad Shai'
__project__ = 'kookoo'

import os
import sys
import time
import requests
import urllib3

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)

from client.client_logger import log
from client.functions_exector import FunctionExector
from common.HTTPResponseCodes import ResponseCode
from common.SettingsHandler import SettingsHandler


class HTTPClient(object):
    """
    Responsible of sending request for new command and sending the response of command using executors threads
    """
    def __init__(self):
        self.cert_path = os.path.join(os.path.join(ROOT_DIR, 'common'), 'cert')
        self.settings_handler = SettingsHandler()
        ip, port = self.settings_handler.get_setting("Server", "ip"), self.settings_handler.get_setting("Server", "port")
        self._uri_get_command = 'https://{}:{}/{}'.format(ip, port, "GetFunction")
        self._uri_response_function = 'https://{}:{}/{}'.format(ip, port, "SendResponse")
        self._get_function_time_interval = self.settings_handler.get_setting("Client", "get_function_interval",
                                                                             value_type='int')

        self.function_executor = FunctionExector()

    def send_response(self, func_name, content):
        """
        Send output command to server
        :return:
        """
        try:
            data_response = "Client Executed function '{}' successfully. {result}".format(
                func_name, result="Result: {}".format(content) if content else "")
            log.info("Sending response of function '{}' ".format(func_name))
            response = requests.post(url=self._uri_response_function,
                                     data=data_response, verify=os.path.join(self.cert_path, "cert.pem"))
            if response.status_code == ResponseCode.OK.value:
                text = response.text
                log.info(text)
            elif response.status_code == ResponseCode.BAD_REQUEST:
                log.error("client request data is not valid")
            elif response.status_code == ResponseCode.BAD_METHOD:
                log.error("client's method is not valid")
            elif response.status_code == ResponseCode.SERVER_ERROR:
                log.error("unexpected error from server")
            else:
                log.error("Unknown Error. response code is: {}".format(response.status_code))
        except Exception as e:
            print("Error in sending response to server. Reason: {}".format(str(e)))

    def run(self):
        """
        Main loop of sending request for new commands from server every interval of time
        :return:
        """
        log.info("**** Starting HTTP Client ****")
        while True:
            try:
                log.info("Sending request : {}".format(self._uri_get_command))
                response = requests.get(url=self._uri_get_command, verify=os.path.join(self.cert_path, "cert.pem"))
                if response.status_code == ResponseCode.OK.value:
                    if not response.content:
                        log.info("No function from Server")
                    else:
                        function_name = response.content
                        log.info("Received new function: '{}'".format(function_name))
                        res = self.function_executor.execute_function(function_name)
                        log.info("Function executed successfully")
                        self.send_response(response.content, res)
                elif response.status_code == ResponseCode.BAD_REQUEST:
                    log.error("client request data is not valid")
                elif response.status_code == ResponseCode.BAD_METHOD:
                    log.error("client's method is not valid")
                elif response.status_code == ResponseCode.SERVER_ERROR:
                    log.error("unexpected error from server")
                else:
                    log.error("Unknown Error. response code is: {}".format(response.status_code))
            except RuntimeError as e:
                log.error("Failure in executing command. Reason: {}".format(str(e)))
            except Exception as e:
                log.error("Failure in sending request to server. Reason: {}".format(str(e)))
            finally:
                time.sleep(self._get_function_time_interval)