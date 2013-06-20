"""
.. module:: facio.start
   :synopsis: Starts the Facio template process.
"""

from .config import Config
from .template import Template

from clint.textui import puts, indent
from clint.textui.colored import green


class Start(object):

    def start(self):
        self.load_config()
        self.process_template()

        with indent(4, quote=' >'):
            puts(green('Done'))

    def load_config(self):
        self.config = Config()

    def process_template(self):
        self.template = Template(self.config)
        self.template.copy_template()
