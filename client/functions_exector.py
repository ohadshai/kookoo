__author__ = 'Ohad Shai'
__project__ = 'kookoo'

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from client.client_logger import log


class FunctionExector(object):

    def __init__(self):
        pass

    def __str__(self):
        return "FunctionExector"

    def execute_function(self, func_name, *args, **kwargs):
        """"""
        func = getattr(self, func_name, None)
        if func is None:
            raise RuntimeError(
                "%s has no '%s' method" % (self, func_name))
        log.info("Executing function '{}'".format(func_name))
        return func(*args, **kwargs)

    def hello_world(self):
        log.info("Hello World")

    def get_fibonacci_10(self):
        def F(n):
            if n == 0:
                return 0
            elif n == 1:
                return 1
            else:
                return F(n - 1) + F(n - 2)
        n = 10
        res = F(n)
        log.info("Fibonacci result for the number {}: {}".format(n, res))
        return res


