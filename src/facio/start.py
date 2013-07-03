# -*- coding: utf-8 -*-

"""
.. module:: facio.start
   :synopsis: Starts the Facio template process.
"""

from .config import Settings, CommandLineInterface, ConfigurationFile
from .template import Template

from clint.textui import puts, indent
from clint.textui.colored import blue, green


class Start(object):

    def start(self):

        interface = CommandLineInterface()
        interface.start()

        config = ConfigurationFile()
        parsed = config.read()

        settings = Settings(interface, parsed)

        template = Template(
            settings.get_project_name(),
            settings.get_template_path()
        )

        template.update_ignore_globs(settings.get_variables())
        template.update_ignore_globs(settings.get_ignore_globs())

        template.copy()
        template.rename()

        with indent(4, quote=' >'):
            puts(green('Done'))
