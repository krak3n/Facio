#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
import os
import re
import sys

from random import choice
from skeletor.opts import Option, OptionParser


class Config(object):

    venv_create = False
    has_config = False
    force_defaut_template = False
    choose_template = False

    templates = {
        'default': 'git+git@github.com:krak3n/Skeletor-Default-Template.git', }

    config_path = os.path.join(os.path.expanduser('~'), '.skeletor.cfg')

    valid_config_sections = {
        'misc': ['install', ],
        'template': [],
        'database': ['db_create', 'db_root_user',
            'db_root_pass'],  # TODO: Remove This - Depreciated
        'virtualenv': ['venv_create', 'venv_path', 'venv_use_site_packages'],
    }

    valid_cl_options = ['project_name', 'install', 'template',
                        'template_settings_dir', 'choose_template',
                        'db_create', 'db_user', 'db_pass', 'db_name',
                        'venv_create', 'venv_path', 'venv_use_site_packages',
                        'venv_prefix', 'variables']

    def __init__(self, use_cfg=True, config_path=None):
        '''Constructor, setup default properties.'''

        self.use_cfg = use_cfg  # Use ~/.skeletor.cfg for config
        if self.use_cfg and config_path:
            self.config_path = config_path  # Override config_path for tests

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
                   help='Install the project onto your path, e.g '
                        'python setup.py develop'),
            # Template Options
            Option('-t', '--template', dest='template', action='store',
                   help='Path to your custom template, absolute paths only '
                        ', git repositories can also be specified by '
                        'prefixing with git+ for example: git+git@gitbub.com'
                        '/path/to/repo.git', type="string"),
            Option('-s', '--template_settings_dir', action='store',
                   help='Template settings directory name', type="string"),
            Option('-c', '--choose_template', dest='choose_template',
                   help="If you have more than 1 template defined use this "
                        "flag to override the default template, Note: "
                        "specifying -t (--template) will mean this "
                        "flag is ignored.", action='store_true', default=None),
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
                   default=None, help='Create python vittual environment '
                                      'without --no-site-packages'),
            Option('--vars', dest='variables', action='store', default=None,
                   help='Custom variables, e.g --vars hello=world,sky=blue'),
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
                if option == 'template':
                    self.templates['default'] = value
                    self.force_defaut_template = True
                else:
                    setattr(self, option, value)

    def load_config(self):
        '''Load users skeletor.cfg if exists.'''

        if os.path.isfile(self.config_path) and self.user_cfg:
            self.config_parser = ConfigParser.ConfigParser()
            self.config_parser.read(self.config_path)
            self.read_config()
            self.has_config = True

    def read_config(self):
        '''Read the skeletor.cfg file and store values.'''

        for section in self.config_parser.sections():
            if section in self.valid_config_sections:
                if section == 'template':
                    self.set_template_options(self.config_parser.items(
                                              'template'))
                else:
                    self.set_attributes(
                        self.valid_config_sections[section],
                        self.config_parser.items(section)
                    )

    def set_template_options(self, items):
        '''Set template options for template choices
        @arg1 list: a list of tuples containing config option name / value
        '''

        if not type(items) == list:
            self.cli_opts.error('It appears the template section in your '
                    '.skeletor.cfg is not configured correctly')
        else:
            for item in items:
                name, value = item
                self.templates[name] = value

    def set_attributes(self, valid_settings, items):
        '''Set class attributes based on valid settings and parsed
        items, items should be the following format:
            [('setting1', 'value1'), [('setting2', 'value2')]
        In, other words, a list of tuples.
        @arg1 list: list of valid settings
        @arg2 list: a list of tuples containing name and value
        '''

        if not type(valid_settings) == list and not type(items) == list:
            self.cli_opts.error('It appears the your .skeletor.cfg is not '
                    'configured correctly')
        else:
            for item in items:
                setting, value = item
                if setting in valid_settings:
                    if value == '0' or value == '1':
                        value = False if value == '0' else True
                    setattr(self, setting, value)

    def validate(self):
        '''Valid provided configuration options.'''

        self.validate_project_name()
        self.validate_template_options()
        self.validate_virtualenv()

    def validate_project_name(self):
        ''' Ensure the project name is alpha numeric and only allows
        userscores. '''

        if not re.match('^\w+$', self.project_name):
            self.cli_opts.error('Project names can only contain numbers'
                    'letters and underscores')

    def validate_virtualenv(self):
        ''' Validate virtualenv settings.'''

        path = getattr(self, 'venv_path', None)
        venv_create = getattr(self, 'venv_create', None)
        if venv_create:
            if not path:
                self.cli_opts.error('You need to provide a virtualenv path '
                                   'where the venv will be created')

    def prompt_template_choice(self):
        '''If the user has multiple templates, prompt them to pick'''

        sys.stdout.write("Please choose a template:\n\n")
        i = 0
        for name in self.templates:
            template = self.templates[name]
            sys.stdout.write("%d) %s: %s\n" % ((i + 1), name, template))
            i += 1
        template_list = list(self.templates)
        while True:
            sys.stdout.write('\nEnter the number for the template: ')
            try:
                num = int(raw_input())
                if num == 0:
                    raise ValueError
                template = self.templates[template_list[num - 1]]
            except (ValueError, IndexError):
                sys.stdout.write('\nPlease choose a number between 1 and '
                                 '%d\n' % len(template_list))
            else:
                return template

    def validate_template_options(self):
        '''Validate template options.'''

        if (self.force_defaut_template
            or len(self.templates) == 1
            or not self.choose_template):
            self.template = self.templates['default']
        else:
            self.template = self.prompt_template_choice()

        if not self.template:
            self.cli_opts.error('You must specify a path to your '
                                'template path')
        else:
            if (not self.template.startswith('git+') and
                not os.path.isdir(self.template)):
                self.cli_opts.error('The path to your template does not '
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
