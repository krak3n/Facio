# -*- coding: utf-8 -*-

"""
.. module:: facio.config
   :synopsis: Facio configuration classes
"""

import os
import re

from clint.textui import puts, indent
from clint.textui.colored import blue, red, yellow
from docopt import docopt
from random import choice
from six.moves import configparser as ConfigParser
from six.moves import input
from textwrap import dedent

from facio import get_version
from facio.exceptions import FacioException


class CommandLineInterface(object):
    """
    Facio

    Facio is a project scaffolding tool originally developed for Django and
    expanded to be framework agnostic. You can use Facio to bootstrap any sort
    of project.

    Documentation:
        https://facio.readthedocs.org

    Usage:
        facio <project_name> [--template <path>|--select] [--vars <variables>]

    Options:
        -h --help              Show this help text.
        --version              Show version.
        -t --template <path>   Template path, can be repository link
                               (git+ / hg+) or a template name defined in
                               ~/.facio.cfg.
        -s --select            Lists templates in ~/.facio.cfg prompting you
                               to select a template from this list.
        --vars <variables>     Comma separated key=value pairs of values to be
                               used in processing templates.

    Example:
        facio hello_world -t git+git@github.com:you/django.git --vars foo=bar
    """

    def start(self):
        self.arguments = docopt(
            dedent(self.__doc__),
            version='Facio {0}'.format(get_version()))
        self.validate_project_name(self.arguments.get('<project_name>'))

    def validate_project_name(self, name):
        if not re.match('^\w+$', name):
            raise FacioException('Project names can only contain numbers '
                                 'letters and underscores')
        return True


class ConfigurationFile(object):
    """ Load the ~/.facio.cfg ini style configuration file, providing an
    easily queryable dict representation of the config attributes. """

    def exists(self, name):
        """ Checks if the .facio.cfg file exists.

        :param name: The file name to read in the users home dir
        :type name: str

        :returns: Bool -- file existence status
        """

        path = os.path.join(os.path.expanduser('~/{0}'.format(name)))
        if os.path.isfile(path):
            return True
        else:
            return False

    def read(self, name='.facio.cfg'):
        """ Parse the config file using ConfigParser module.

        :param name: The file name to read in the users home dir -- optional
        :type name: str

        :returns: ConfirgParser or bool
        """

        if self.exists(name):
            path = os.path.expanduser('~/{0}'.format(name))
            parser = ConfigParser.ConfigParser()
            try:
                parser.readfp(open(path))
            except ConfigParser.Error:
                raise FacioException('Unable to parse {0}'.format(path))
            else:
                with indent(4, quote=' >'):
                    puts(blue('Loaded {0}'.format(path)))
                return parser
        return False


class Settings(object):

    def __init__(self, interface, config):
        """ Facio settings class. Taking aguments passed into the cli
        interface and configurable options into a single callable
        class.

        :param interface: The docopt command line interface
        :type interface: dict

        :param config: Parsed config file
        :type config: False or ConfigParser object
        """

        self.interface = interface
        self.config = config

    @property
    def project_name(self):
        """ Get the project name from the command line interface.

        :returns: str -- The project name
        """

        try:
            return self.interface.arguments['<project_name>']
        except KeyError:
            raise FacioException('Project name not defined.')

    def get_template_path(self):
        """ Obtain the template with from the command line interface or from
        prompting the user to choose a template from the config file.

        :returns: str or bool
        """

        template = self.interface.arguments.get('--template', False)
        select = self.interface.arguments.get('--select', False)

        try:
            templates = self.config.items('template')
        except ConfigParser.NoSectionError:
            if select:
                raise FacioException('Missing [template] section '
                                     'in Facio configuration file.')
            else:
                template = []

        # Path or template name alias
        if template:
            try:
                path = [p for n, p in templates if n == template][0]
            except IndexError:
                return template
            else:
                return path

        # Select template from configuration file
        if select:
            if self.config:
                tries = 5
                with indent(4, quote=' >'):
                    puts(yellow('Please select a template:'))
                    for i, item in enumerate(templates, start=1):
                        name, path = item
                        puts(blue('{0}) {1}: {2}'.format(i, name, path)))
                    for n in range(1, (tries + 1)):
                        try:
                            prompt = 'Please enter the number of '\
                                     'the template ({0} of {1} tries'\
                                     '): '.format(n, tries)
                            num = int(input(' >  ' + yellow(prompt)))
                            if num == 0:
                                raise ValueError
                            return templates[(num - 1)]
                        except (ValueError, TypeError, IndexError):
                            puts(red('Please enter a valid number'))
                raise FacioException('A template was not selected')
            else:
                raise FacioException('You must create a Facio configuration '
                                     'file to use --select')

        # Default template
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'default_template')

    def get_variables(self):
        """ Returns variables passed into command line interface, if lookup
        fails an empty list is returned.

        :returns: str or None
        """

        return self.interface.arguments.get('--vars')

    def get_file_ignores(self):
        """ Returns list of of file ignore globs from configuration file.

        :returns: list
        """

        try:
            globs = self.config.get('misc', 'ignore')
        except ConfigParser.NoSectionError:
            return []
        else:
            return globs.split(',')

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
