# -*- coding: utf-8 -*-

"""
.. module:: facio.cli
   :synopsis: Facio command line entry point and configuration.
"""

import re
import sys

from docopt import docopt
from facio import get_version


class CLI(object):
    """
    Facio.

    Facio is a project scaffolding tool originally  developed for Django and
    expanded to be framework agnostic. You can use facio to bootstrap any sort
    of project.

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

    def __init__(self):
        self.arguments = docopt(
            self.__doc__,
            version='Facio {0}'.format(get_version()))
        self._validate_project_name()

    def _validate_project_name(self):
        if not re.match('^\w+$', self.arguments.get('<project_name>')):
            sys.exit('Project names can only contain numbers letters and '
                     'underscores')
