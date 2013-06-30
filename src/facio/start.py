# -*- coding: utf-8 -*-

"""
.. module:: facio.start
   :synopsis: Starts the Facio template process.
"""

from .config import Settings, CommandLineInterface, ConfigurationFile
from .template import Template

from clint.textui import puts, indent
from clint.textui.colored import green


class Start(object):

    def start(self):

        interface = CommandLineInterface()
        interface.start()

        config = ConfigurationFile()
        parsed = config.read()

        settings = Settings(interface, parsed)
        path = settings.get_template_path()

        puts(path)

        with indent(4, quote=' >'):
            puts(green('Done'))

    def process_template(self):
        self.template = Template(self.config)
        self.template.copy_template()
