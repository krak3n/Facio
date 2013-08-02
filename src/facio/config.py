# -*- coding: utf-8 -*-

"""
.. module:: facio.config
   :synopsis: Facio configuration classes
"""

import os
import re

from docopt import docopt
from facio import get_version
from facio.base import BaseFacio
from facio.exceptions import FacioException
from facio.state import state
from six.moves import configparser as ConfigParser
from textwrap import dedent


HOOKS_FILE_NAME = '.facio.hooks.yml'
CONFIG_FILE_NAME = '.facio.cfg'


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
        else:
            state.set_project_name(name)


class ConfigurationFile(BaseFacio):
    """ Load the ~/.facio.cfg ini style configuration file, providing an
    easily queryable dict representation of the config attributes. """

    def read(self, name=CONFIG_FILE_NAME):
        """ Parse the config file using ConfigParser module.

        :param name: The file name to read in the users home dir -- optional
        :type name: str

        :returns: ConfirgParser or bool
        """

        path = os.path.expanduser('~/{0}'.format(name))
        parser = ConfigParser.ConfigParser()
        try:
            parser.readfp(open(path))
        except IOError:
            self.warning('{0} Not found'.format(path))
        except ConfigParser.Error:
            raise FacioException('Unable to parse {0}'.format(path))
        else:
            self.out('Loaded {0}'.format(path))
        return parser


class Settings(BaseFacio):

    default_template_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'default')

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

    def get_template_path(self):
        """ Obtain the template with from the command line interface or from
        prompting the user to choose a template from the config file.

        :returns: str or bool
        """

        templates = []
        template = self.interface.arguments.get('--template', False)
        select = self.interface.arguments.get('--select', False)

        try:
            templates = self.config.items('template')
        except ConfigParser.NoSectionError:
            if select:
                raise FacioException('Missing [template] section '
                                     'in Facio configuration file.')

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
            tries = 5
            self.out('Please select a template:')
            for i, item in enumerate(templates, start=1):
                name, path = item
                self.out('{0}) {1}: {2}'.format(i, name, path))
            for n in range(1, (tries + 1)):
                try:
                    prompt = 'Please enter the number of '\
                             'the template ({0} of {1} tries'\
                             '): '.format(n, tries)
                    num = int(self.gather(prompt))
                    if num == 0:
                        raise ValueError
                    name, path = templates[(num - 1)]
                    return path
                except (ValueError, TypeError, IndexError):
                    self.error('Please enter a valid number')
            raise FacioException('A template was not selected')

        # Default template
        return Settings.default_template_path

    def get_variables(self):
        """ Returns dict of variables passed into command line interface.

        :returns: dict
        """

        variable_dict = {}
        variables = self.interface.arguments.get('--vars')
        if variables:
            for pair in variables.split(','):
                key, value = pair.split('=')
                variable_dict[key] = value
        return variable_dict

    def copy_ignore_globs(self):
        """ Returns list of of file copy ignore globs from configuration file.

        :returns: list
        """

        try:
            globs = self.config.get('files', 'copy_ignore')
        except ConfigParser.NoSectionError:
            return []
        except ConfigParser.NoOptionError:
            return []
        else:
            return globs.split(',')

    def render_ignore_globs(self):
        """ Returns list of of file render ignore globs from configuration
        file.

        :returns: list
        """

        try:
            globs = self.config.get('files', 'render_ignore')
        except ConfigParser.NoSectionError:
            return []
        except ConfigParser.NoOptionError:
            return []
        else:
            return globs.split(',')
