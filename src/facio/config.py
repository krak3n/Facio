"""
facio.config
------------

Sets up variables and configuration for Facio from command line and / or
a configuration file.
"""

import ConfigParser
import os
import sys

try:
    from clint.textui import puts, indent
    from clint.textui.colored import blue
except ImportError:
    pass
from random import choice

from .cli import CLIOptions


class ConfigFile(object):

    templates = {}

    sections = {
        'misc': ['install', ],
        'template': [],
        'virtualenv': ['venv_create', 'venv_path', 'venv_use_site_packages'],
    }

    path = os.path.join(os.path.expanduser('~'), '.facio.cfg')

    def __init__(self):
        if os.path.isfile(self.path):
            self._parse_config()
        else:
            self.cfg_loaded = False

    def _parse_config(self):
        self.parser = ConfigParser.ConfigParser()
        try:
            self.parser.read(self.path)
        except ConfigParser.MissingSectionHeaderError:
            self.cfg_loaded = False
            # TODO: print warning to user
        except ConfigParser.ParsingError:
            # TODO: print warning to user
            self.cfg_loaded = False
        else:
            self.cfg_loaded = True
            with indent(4, quote=' >'):
                puts(blue('Loaded ~/.facio.cfg'))
            for section in self.sections:
                try:
                    items = self.parser.items(section)
                except ConfigParser.NoSectionError:
                    pass
                else:
                    if section == 'template':
                        self._add_templates(items)
                    else:
                        self._set_attributes(section, items)

    def _add_templates(self, items):
        for item in items:
            name, value = item
            self.templates[name] = value

    def _set_attributes(self, section, items):
        opts = self.sections[section]
        for opt in opts:
            try:
                opt, val = [(x, y) for x, y in items if x == opt][0]
            except IndexError:
                pass
            else:
                if val == '0' or val == '1':
                    val = False if val == '0' else True
                setattr(self, opt, val)


class Config(object):

    default_template = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'default_template')

    def __init__(self):
        self.cli_args = CLIOptions()
        self.file_args = ConfigFile()
        self.django_secret_key

    def _error(self, msg):
        self.cli_args._parser.error(msg)

    #
    # Project Properties
    #

    @property
    def project_name(self):
        return self.cli_args.project_name

    #
    # Template Properties
    #

    def _validate_template_options(self):
        if (not self._tpl.startswith('git+') and
                not os.path.isdir(self._tpl)):
            self._error('The path to your template does not exist.')

    def _template_choice_prompt(self):
        templates = self.file_args.templates
        max_tries = 5
        template_list = list(templates)
        i = 0
        sys.stdout.write("Please choose a template:\n\n")
        for name in templates:
            template = templates[name]
            sys.stdout.write("{0}) {1}: {2}\n".format((i + 1), name, template))
            i += 1
        i = 1
        while True:
            if i > max_tries:
                self._error('You failed to enter a valid template number.')
            try:
                num = int(raw_input(
                    '\nEnter the number for the template '
                    '({0} of {1} tries): '.format(i, max_tries)))
                if num == 0:
                    raise ValueError
                template = templates[template_list[num - 1]]
            except (ValueError, IndexError):
                sys.stdout.write('\nPlease choose a number between 1 and '
                                 '{0}\n'.format(len(template_list)))
                i += 1
            else:
                return template

    @property
    def _cli_template(self):
        try:
            return self.cli_args.template
        except AttributeError:
            return False

    @property
    def _cli_choose_template(self):
        try:
            return self.cli_args.choose_template
        except AttributeError:
            return False

    @property
    def template(self):
        if not getattr(self, '_tpl', None):
            if self._cli_template:
                self._tpl = self._cli_template
            elif self._cli_choose_template:
                self._tpl = self._template_choice_prompt()
            else:
                try:
                    self._tpl = self.file_args.templates['default']
                except KeyError:
                    self._tpl = self.default_template
        self._validate_template_options()
        return self._tpl

    @property
    def template_settings_dir(self):
        try:
            return self.cli_args.template_settings_dir
        except AssertionError:
            return False

    @property
    def variables(self):
        try:
            return self.cli_args.variables
        except AssertionError:
            return False

    #
    # Python Properties (Experimental)
    #

    @property
    def _file_args_install(self):
        try:
            return self.file_args.install
        except AttributeError:
            return False

    @property
    def _cli_args_install(self):
        try:
            return self.cli_args.install
        except AttributeError:
            return False

    @property
    def install(self):
        if self._cli_args_install or self._file_args_install:
            return True
        return False
    #
    # Virtual Environment Properties (Experimental)
    #

    def _validate_virtualenv_options(self):
        if not self.venv_path:
            self._error('You need to provide a virtualenv path where the '
                        'venv will be created')

    @property
    def _file_args_venv_create(self):
        try:
            return self.file_args.venv_create
        except AttributeError:
            return False

    @property
    def _cli_args_venv_create(self):
        try:
            return self.cli_args.venv_create
        except AttributeError:
            return False

    @property
    def _file_args_venv_path(self):
        try:
            return self.file_args.venv_path
        except AttributeError:
            return False

    @property
    def _cli_args_venv_path(self):
        try:
            return self.cli_args.venv_path
        except AttributeError:
            return False

    @property
    def _file_args_venv_use_site_packages(self):
        try:
            return self.file_args.venv_use_site_packages
        except AttributeError:
            return False

    @property
    def _cli_args_venv_use_site_packages(self):
        try:
            return self.cli_args.venv_use_site_packages
        except AttributeError:
            return False

    @property
    def venv_create(self):
        if self._cli_args_venv_create or self._file_args_venv_create:
            self._validate_virtualenv_options()
            return True
        return False

    @property
    def venv_path(self):
        if self._file_args_venv_path and not self._cli_args_venv_path:
            return self._file_args_venv_path
        elif self._cli_args_venv_path:
            return self.cli_args.venv_path
        return False

    @property
    def venv_use_site_packages(self):
        if (self._cli_args_venv_use_site_packages
                or self._file_args_venv_use_site_packages):
            return True
        return False

    @property
    def venv_prefix(self):
        try:
            return self.cli_args.venv_prefix
        except AttributeError:
            return False

    #
    # Django Secret Key Generation
    #

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
