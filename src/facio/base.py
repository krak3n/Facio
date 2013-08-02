# -*- coding: utf-8 -*-

"""
.. module:: facio.base
   :synopsis: Base facio classes.
"""

from clint.textui import puts, indent
from clint.textui.colored import blue, green, red, yellow
from six.moves import input


class BaseFacio(object):

    def out(self, message, color=blue):
        """ Print message information to user (Blue)

        :param message: Message to print to user
        :type message: str

        ** Optional Key Word Arguments **

        :param color: Clint color function to use
        :type: function -- default blue
        """

        with indent(4, quote=' >'):
            puts(color(message))

    def success(self, message):
        """ Print a success message (Green)

        :param message: Message to print to user
        :type message: str
        """

        return self.out(message, color=green)

    def warning(self, message):
        """ Print a warning message (Yellow)

        :param message: Message to print to user
        :type message: str
        """

        message = 'Warning: {0}'.format(message)
        return self.out(message, color=yellow)

    def error(self, message):
        """ Print error that does not result in an exit (Red)

        :param message: Message to print to user
        :type message: str
        """

        message = 'Error: {0}'.format(message)
        return self.out(message, color=red)

    def gather(self, message):
        """ Common message prompting for gathering input form the end user.

        :param message: Message to print to user
        :type message: str
        """

        return input(' >  ' + yellow(message))
