__author__ = 'Ohad Shai'
__project__ = 'kookoo'

import os
import sys


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from logger import KookooLogger

log = KookooLogger("Server").get_logger()
