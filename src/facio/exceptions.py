# -*- coding: utf-8 -*-

"""
.. module:: facio.exceptions
   :synopsis: Custom Facio exception classes
"""

import sys

from clint.textui import indent, puts
from clint.textui.colored import red


class FacioException(Exception):

    def __init__(self, message):
        with indent(4, quote=' >'):
            puts(red('Error: {0}'.format(message)))
            puts(red('Exiting'))
        sys.exit()
