"""
facio.cli
---------

Prompt user to enter options for Facio, determines how Facio behaves. Options
are split into 3 groups:
- Project Options
- Template Options
- Experimental Options
"""


import optparse
import re

from . import __version__


class CLIOptions(object):

    MANDATORY_OPTS = ['project_name', ]

    def __init__(self):
        self._parser = optparse.OptionParser(
            usage='Usage: %prog -n <project_name> <options>',
            version='%prog version {0}'.format(__version__),
            description='Facio is a project scaffolding tool origionally '
                        'developed for Django and expanded to be framework '
                        'agnostic. You can use facio to bootstrap any sort '
                        'of project.',
            epilog='Example: facio -n hello_world -c --vars foo=bar')
        self._add_project_options()
        self._add_template_options()
        self._add_experimental_options()
        self.opts, self.args = self._parser.parse_args()
        self._validate()

    def __getattr__(self, name):
        opt = getattr(self.opts, name, None)
        if not opt is None:
            return opt
        else:
            raise AttributeError

    def _add_project_options(self):
        group = optparse.OptionGroup(self._parser, 'Project Options')
        group.add_option('-n', '--name', dest='project_name',
                         help='The Project Name (Mandatory), only use '
                              'alphanumeric chracters and underscores.',
                         type='string', metavar='<ARG>')
        self._parser.add_option_group(group)

    def _add_template_options(self):
        group = optparse.OptionGroup(self._parser, 'Template Options')
        group.add_option('-t', '--template', dest='template', action='store',
                         help='Path to your custom template, absolute paths '
                         'only , git repositories can also be specified by '
                         'prefixing with git+ for example: git+git@gitbub.com'
                         '/path/to/repo.git', type='string', metavar='<ARG1>')
        group.add_option('-c', '--choose_template', dest='choose_template',
                         help='If you have more than 1 template defined use '
                         'this flag to override the default template, Note: '
                         'specifying -t (--template) will mean this '
                         'flag is ignored.', action='store_true',
                         default=False)
        group.add_option('-s', '--template_settings_dir', action='store',
                         help='Template settings directory name',
                         type='string', metavar='<ARG>')
        group.add_option('--vars', dest='variables', action='store',
                         default=False, help='Custom variables, e.g --vars '
                         'hello=world,sky=blue', metavar='<ARG>'),
        self._parser.add_option_group(group)

    def _add_experimental_options(self):
        group = optparse.OptionGroup(self._parser, 'Experimental Options')
        group.add_option('-i', '--install', action='store_true', default=False,
                         help='Install the project onto your path, e.g '
                         'python setup.py develop'),
        group.add_option('-e', '--venv_create', dest='venv_create',
                         action='store_true', default=False,
                         help='Create python virtual environment'),
        group.add_option('-p', '--venv_path', dest='venv_path', action='store',
                         help='Python virtualenv home directory',
                         type='string', metavar='<ARG>'),
        group.add_option('-S', '--venv_use_site_packages',
                         dest='venv_use_site_packages', action='store_true',
                         default=False, help='Create python vittual '
                         'environment without --no-site-packages'),
        group.add_option('-x', '--venv_prefix', dest='venv_prefix',
                         action='store',
                         help='Virtual environment name prefix',
                         type='string', metavar='<ARG>')
        self._parser.add_option_group(group)

    def _validate(self):
        self._validate_required()
        self._validate_project_name()

    def _validate_required(self):
        for opt in self.MANDATORY_OPTS:
            if not getattr(self.opts, opt, None):
                self._parser.error('A mandatory option is missing, see --help')

    def _validate_project_name(self):
        if not re.match('^\w+$', self.opts.project_name):
            self._parser.error('Project names can only contain numbers'
                               'letters and underscores')
