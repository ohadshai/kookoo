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
        """
        Prints 'Hello World'
        :return:
        """
        log.info("Hello World")

    def add(self, x, y):
        """
        Adds two numbers
        :param x:
        :param y:
        :return:
        """
        return x + y

    def subtract(self, x, y):
        """
        Subtracts two numbers
        :param x:
        :param y:
        :return:
        """
        return x - y

    def multiply(self, x, y):
        """
        Multiplies two numbers
        :param x:
        :param y:
        :return:
        """
        return x * y

    def divide(self, x, y):
        """
        Divides two numbers
        :param x:
        :param y:
        :return:
        """
        return x / y

    def pow_2(self, n):
        """
        Returns the power of n in 2
        :param x:
        :param y:
        :return:
        """
        return n**2

    def fibonacci(self, n):
        """
        Calculates fibonachi result according to n
        :param n:
        :return:
        """
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fibonacci(n - 1) + self.fibonacci(n - 2)


