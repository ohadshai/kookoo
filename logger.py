__author__ = 'Ohad Shai'
__project__ = 'kookoo'

import os
import logging
import logging.handlers as handlers
import sys

from common.SettingsHandler import SettingsHandler

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(ROOT_DIR, 'kookoo.log')


class KookooLogger(object):
    """
    Responsible with logging to log file and to stdout
    """
    def __init__(self, name, path=LOG_PATH):
        self.settings_handler = SettingsHandler()
        self.logger = logging.getLogger(name)
        log_level = getattr(logging, self.settings_handler.get_setting("Logger", "log_level").upper(), None)
        if not log_level:
            log_level = logging.INFO
        self.logger.setLevel(log_level)
        self.log_handler = handlers.TimedRotatingFileHandler(path, when='w5', interval=1, backupCount=4)
        self.stdout_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
        self.log_handler.setFormatter(formatter)
        self.stdout_handler.setFormatter(formatter)
        self.logger.addHandler(self.log_handler)
        self.logger.addHandler(self.stdout_handler)

    def get_logger(self):
        return self.logger
