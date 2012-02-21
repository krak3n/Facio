#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
import os
import urllib2
from random import choice
from skeletor.opts import Option, OptionParser

class Config(object):

    has_config = False
    template_path = 'git+git@github.com:krak3n/Skeletor-Default-Template.git'
    config_path = os.path.join(os.path.expanduser('~'),
                                   '.skeletor.cfg')

    valid_config_sections = {
        'misc': ['install',],
        'template': ['template_path', 'template_settings_dir'],
        'database': ['db_create', 'db_root_user', 'db_root_pass'],
        'virtualenv': ['venv_create', 'venv_path', 'venv_use_site_packages'],
    }

    valid_cl_options = ['project_name', 'install', 'template_path',
                        'template_settings_dir', 'db_create', 'db_user',
                        'db_pass', 'db_name', 'venv_create', 'venv_path',
                        'venv_use_site_packages', 'venv_prefix']

    def __init__(self):
        '''Constructor, setup default properties.'''

        self.load_config()
        self.set_command_line_options()
        self.validate()

    def set_command_line_options(self):
        '''Set command line options.'''

        opt_list = [
            # Project Name
            Option('-n', '--name', dest='project_name', action='store',
                   help='Your project name', required=True, type="string"),
            # Install the new project onto the path
            Option('-i', '--install', action='store_true', default=False,
                   help='Install the project onto your path, e.g '\
                        'python setup.py develop'),
            # Template Options
            Option('-t', '--template', dest='template_path', action='store',
                   help='Path to your custom template', type="string"),
            Option('-s', '--template_settings_dir', action='store',
                   help='Template settings directory name', type="string"),
            # Database Option
            Option('-d', '--db_create', action="store_true", default=None,
                   help='Create database'),
            Option('-N', '--db_name', dest='db_name', action='store',
                   help='Database name', type='string'),
            Option('-u', '--db_user', dest='db_user', action='store',
                   help='Database user name', type='string'),
            Option('-p', '--db_pass', dest='db_pass', action='store',
                   help='Database user password', type='string'),
            # Virtual Env Options
            Option('-E', '--venv_create', dest='venv_create',
                   action='store_true', default=None,
                   help='Create python virtual environment'),
            Option('-P', '--venv_path', dest='venv_path', action='store',
                   help='Python Virtualenv home directory', type='string'),
            Option('-S', '--venv_use_site_packages',
                   dest='venv_use_site_packages', action='store_true',
                   default=None, help='Create python vittual environment '\
                                      'without --no-site-packages'),
            Option('-x', '--venv_prefix', dest='venv_prefix', action='store',
                   help='Virtual environment prefix', type='string')]

        self.cli_opts = OptionParser(option_list=opt_list)
        self.set_attributes_from_command_line()

    def set_attributes_from_command_line(self):
        '''Set attibutes that have been parsed via command line.'''

        (cl_options, cl_args) = self.cli_opts.parse_args()

        for option in self.valid_cl_options:
            value = getattr(cl_options, option, None)
            if value:
                setattr(self, option, value)

    def load_config(self):
        '''Load users skeletor.cfg if exists.'''

        if os.path.isfile(self.config_path):
            self.config_parser = ConfigParser.ConfigParser()
            self.config_parser.read(self.config_path)
            self.read_config()
            self.has_config = True

    def read_config(self):
        '''Read the skeletor.cfg file and store values.'''

        for section in self.config_parser.sections():
            if section in self.valid_config_sections:
                self.set_attributes(
                    self.valid_config_sections[section],
                    self.config_parser.items(section)
                )

    def set_attributes(self, valid_settings, items):
        '''Set class attributes based on valid settings and parsed
        items, items should be the following format:
            [('setting1', 'value1'), [('setting2', 'value2')]
        In, other words, a list of tuples.
        @arg1 list: list of valid settings
        @arg2 list: a list of tuples containing name and value
        '''

        if not type(valid_settings) == list and not type(items) == list:
            raise Exception
        else:
            for item in items:
                setting, value = item
                if setting in valid_settings:
                    if value == '0' or value == '1':
                        value = False if value == '0' else True
                    setattr(self, setting, value)

    def validate(self):
        '''Valid provided configuration options.'''

        self.validate_db_options()
        self.validate_virtualenv()

    def validate_db_options(self):
        '''Validate provided database options.'''

        db_create = getattr(self, 'db_create', None)
        # New DB setitngs - set by command line
        db_name = getattr(self, 'db_name', None)
        db_user = getattr(self, 'db_user', None)
        db_pass = getattr(self, 'db_pass', None)
        # DB Root settings, set in skeletor.cfg
        db_root_user = getattr(self, 'db_root_user', None)
        db_root_pass = getattr(self, 'db_root_pass', None)

        if db_create:
            if not db_root_user or not db_root_pass:
                self.cli_opts.error('You need to provide dataase root '\
                                    'user and password in your .skeletor.cfg')
            else:
                if not db_name or not db_user or not db_pass:
                    self.cli_opts.error('You need to provide a database '\
                                        'user, password & name for creating '\
                                        'databases')

    def validate_virtualenv(self):
        ''' Validate virtualenv settings.'''

        path = getattr(self, 'venv_path', None)
        if self.venv_create:
            if not path:
                self.cli_opts.error('You need to provide a virtualenv path '\
                                   'where the venv will be created')

# TODO: Databse creation not yet working
    def validate_template_options(self):
        '''Validate template options.'''

        print 'Warning: Database creation is not yet supported'

        template_path = getattr(self, 'template_path', None)

        if not template_path:
            self.cli_options.error('You must specify a path to your '\
                                   'template path')
        else:
            if not os.path.isfile(template_path):
                self.cli_options.error('The path to your template does not '\
                                       'exist.')

    @property
    def django_secret_key(self):
        '''Generate a secret key for Django Projects.'''

        if hasattr(self, 'generated_django_secret_key'):
            return self.generated_django_secret_key
        else:
            choice_str = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            key = ''.join([choice(choice_str) for i in range(50)])
            self.generated_django_secret_key = key
            return key
