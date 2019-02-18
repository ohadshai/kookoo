__author__ = 'Ohad Shai'
__project__ = 'kookoo'

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from client.http_client import HTTPClient

if __name__ == '__main__':
    client = HTTPClient()
    client.run()