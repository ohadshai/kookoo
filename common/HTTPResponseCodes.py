from enum import Enum


class ResponseCode(Enum):
    OK = 200
    BAD_REQUEST = 400
    BAD_METHOD = 405
    SERVER_ERROR = 500
