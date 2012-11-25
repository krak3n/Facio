#!/usr/bin/env python
# encoding: utf-8

__version__ = '1.0Beta1'

from .config import Config
from .install import Install
from .template import Template
from .virtualenv import Virtualenv


class Skeletor(object):

    def __init__(self):
        '''Constructor, fires all required methods.'''

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
