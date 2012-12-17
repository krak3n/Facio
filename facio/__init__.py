"""
facio.__init__
--------------

This kicks the whole thing off, fireing CLI option prompt and processing
the template.
"""

__version__ = '1.0.1'

from clint.textui import puts

from .config import Config
from .install import Install
from .template import Template
from .virtualenv import Virtualenv


class Facio(object):

    def __init__(self):
        '''Constructor, fires all required methods.'''

        puts('Facio - Project scaffolfding')
        puts('----------------------------')

        # Basic Skeleton Generation
        self.config = Config()
        self.template = Template(self.config)
        self.template.copy_template()

        # Create python virtual environment
        if self.config.venv_create:
            self.venv = Virtualenv(self.config)

        # Install the project to python path
        if hasattr(self.config, 'install'):
            if self.config.install:
                self.install = Install(self.config,
                                       self.template,
                                       getattr(self, 'venv', None))
