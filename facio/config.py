"""
facio.config
------------

Sets up variables and configuration for Facio from command line and / or
a configuration file.
"""

import ConfigParser
import os
import sys

from random import choice


class Config(object):

    venv_create = False
    force_defaut_template = False
    choose_template = False

    templates = {
        'default': os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'default_template'), }

    config_path = os.path.join(os.path.expanduser('~'), '.facio.cfg')

    valid_config_sections = {
        'misc': ['install', ],
        'template': [],
        'virtualenv': ['venv_create', 'venv_path', 'venv_use_site_packages'],
    }

    def __init__(self, cli):
        '''Constructor, setup default properties.'''

        self.cli = cli
        self.project_name = cli.project_name
        self.load_config()

    def load_config(self):
        '''Load users facio.cfg if exists.'''

        if os.path.isfile(self.config_path):
            self.config_parser = ConfigParser.ConfigParser()
            self.config_parser.read(self.config_path)
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
            self.cli.error('It appears the template section in your '
                           '.facio.cfg is not configured correctly')
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
            self.cli.error('It appears the your .facio.cfg is not '
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

        self.validate_template_options()
        self.validate_virtualenv()

    def validate_virtualenv(self):
        ''' Validate virtualenv settings.'''

        path = getattr(self, 'venv_path', None)
        venv_create = getattr(self, 'venv_create', None)
        if venv_create and not path:
            self.cli.error('You need to provide a virtualenv path '
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
        max_tries = 5
        i = 1
        while True:
            if i > max_tries:
                self.cli.error('You failed to enter a valid template number.')
            try:
                num = int(raw_input('\nEnter the number for the template '
                                    '(%d of %d tries): ' % (i, max_tries)))
                if num == 0:
                    raise ValueError
                template = self.templates[template_list[num - 1]]
            except (ValueError, IndexError):
                sys.stdout.write('\nPlease choose a number between 1 and '
                                 '%d\n' % len(template_list))
                i += 1
            else:
                return template

    def validate_template_options(self):
        '''Validate template options.'''

        if (self.force_defaut_template or len(self.templates) == 1
                or not self.choose_template):
            self.template = self.templates['default']
        else:
            self.template = self.prompt_template_choice()

        if (not self.template.startswith('git+') and
                not os.path.isdir(self.template)):
            self.cli.error('The path to your template does not exist.')

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
