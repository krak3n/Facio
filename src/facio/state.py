# -*- coding: utf-8 -*-

"""
.. module:: facio.state
   :synopsis: Facio state module, for accessing and maintaining state during
              the template generation process.
"""

from facio.base import BaseFacio
from six.moves import builtins


class State(BaseFacio):

    def __init__(self):
        """ State is stored in a __facio__ super global set at the moment
        this class is instantiated but only if not already set.
        """

        try:
            self.state = builtins.__facio__
        except AttributeError:
            builtins.__facio__ = self
            self.state = builtins.__facio__

state = State()
