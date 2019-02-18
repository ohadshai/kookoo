import os
import sys
import random

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

FUNCTIONS_FILE_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "functions.txt")


class FunctionsHandler(object):
    """
    Responsible to load functions name and give at random
    """
    def __init__(self):
        self._file_path = FUNCTIONS_FILE_PATH
        self._function_names = []

    def get_functions_from_file(self):
        try:
            with open(self._file_path) as f:
                for function in f.readlines():
                    self._function_names.append(function.strip('\n'))

        except FileNotFoundError as e:
            print("File of functions doesn't exists on: {}".format(self._file_path))

    def get_random_function(self):
        return self._function_names[random.randint(0, len(self._function_names) - 1)]
