# -*- coding: utf-8 -*-

"""
.. module:: facio.config
   :synopsis: Facio configuration classes
"""

import os
import sys

from clint.textui import puts, indent
from clint.textui.colored import blue, red
from random import choice
from six.moves import configparser as ConfigParser
from six.moves import input

from .cli import CLI


class ConfigFile(object):

    templates = []

    sections = {
        'template': [],
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
            self.templates.append((name, value))

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
        self.cli_args = CLI()
        self.file_args = ConfigFile()
        self.django_secret_key

    def _error(self, msg):
        raise SystemExit(red(msg))

    #
    # Project Properties
    #

    @property
    def project_name(self):
        return self.cli_args.arguments.get('<project_name>')

    #
    # Template Properties
    #

    def _validate_template_options(self):
        templates = self.file_args.templates
        try:
            self._tpl = [t for n, t in templates if n == self._tpl][0]
        except IndexError:
            pass  # We don't care if this fails, assume it's a path
        if (not self._tpl.startswith('git+') and
                not self._tpl.startswith('hg+') and
                not os.path.isdir(self._tpl)):
            self._error('The path to your template does not exist.')

    def _template_choice_prompt(self):
        templates = self.file_args.templates
        max_tries = 5
        i = 0
        sys.stdout.write("Please choose a template:\n\n")
        for name, template in templates:
            sys.stdout.write("{0}) {1}: {2}\n".format((i + 1), name, template))
            i += 1
        i = 1
        while True:
            if i > max_tries:
                self._error('You failed to enter a valid template number.')
            try:
                num = int(input(
                    '\nEnter the number for the template '
                    '({0} of {1} tries): '.format(i, max_tries)))
                if num == 0:
                    raise ValueError
                name, template = templates[num - 1]
            except (ValueError, IndexError):
                sys.stdout.write('\nPlease choose a number between 1 and '
                                 '{0}\n'.format(len(templates)))
                i += 1
            else:
                return template

    @property
    def _cli_template(self):
        try:
            return self.cli_args.arguments.get('--template')
        except KeyError:
            return False

    @property
    def _cli_choose_template(self):
        try:
            return self.cli_args.arguments.get('--select')
        except KeyError:
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
                    self._tpl = [t for n, t
                                 in self.file_args.templates
                                 if n == 'default'][0]
                except IndexError:
                    self._tpl = self.default_template
        self._validate_template_options()
        return self._tpl

    @property
    def variables(self):
        try:
            return self.cli_args.arguments.get('--vars')
        except KeyError:
            return False

    @property
    def ignore(self):
        try:
            globs = self.file_args.ignore
        except AttributeError:
            return []
        else:
            return globs.split(',')

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
