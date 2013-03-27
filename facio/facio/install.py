"""
facio.install
-------------

This experimental. This should install a python template onto the path
in develop mode.
"""

import os

from shutil import rmtree
from subprocess import Popen, PIPE, STDOUT


class Install(object):

    def __init__(self, config, template, venv):
        '''Install the new prpject on the python path.'''

        self.config = config
        self.template = template
        self.venv = venv
        self.install()

    @property
    def is_django(self):
        '''Is this a django project, skeleton should contain .isdjango
        file in skeleton root.'''

        if (os.path.isfile(os.path.join(self.template.project_root,
                                        '.isdjango'))):
            return True
        else:
            return False

#TODO: Ripe for a refactor
    def validate(self):
        '''Validate we can install onto the path.'''

        project = self.config.project_name

        if self.venv:
            virtualenv_path = self.venv.venv_path
            self.executable = os.path.join(virtualenv_path, 'bin', 'python')
        else:
            if os.environ.get('VIRTUAL_ENV'):
                print 'Warning: You have an active virtual environment '\
                      'installing to %s virtual environment.' % (
                          os.environ.get('VIRTUAL_ENV'))
            cmd = 'which python'
            p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
                      close_fds=True)
            output = p.stdout.read()
            if output == '':
                self.config._error('Unable to locate python executable')
                return False
            self.executable = output.rstrip()

        if not os.path.exists(self.executable):
            self.config._error('Unable to find python executable at {0}, '
                               'not able to install %s to the virtual '
                               'env' % (self.executable, project))

        # Check the new package name is not already one installed on the path
        cmd = "%s -c 'import %s'" % (self.executable, project)
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
                  close_fds=True)
        output = p.stdout.read()

        import_error = False
        for line in output.splitlines():
            if "ImportError: No module named %s" % project in line:
                import_error = True

        if not import_error:
            self.config._error('A package with %s name already '
                               'exists, cannot install' % (project))
            return False

        # Check the project as a setup.py
        has_setup = False
        for file in os.listdir(self.template.project_root):
            if file == 'setup.py':
                self.setup_path = os.path.join(self.template.project_root,
                                               file)
                has_setup = True

        if not has_setup:
            self.config._error('There is no setup.py in the project root, '
                               'cannot install project.')
            return False

        return True

    def install(self):
        '''Install the new project onto the path.'''

        if self.validate():
            os.chdir(self.template.project_root)
            cmd = '%s %s develop' % (self.executable, self.setup_path)
            os.system(cmd)
            rmtree(os.path.join(self.template.project_root,
                                '%s.egg-info' % self.config.project_name))

            self.update_post_activate()

# TODO: This could be configurable
# TODO: want to add export DJANGO_SETTINGS_MODUAL=foo.bar.thing
    def update_post_activate(self):
        '''Update post activate script to cd into working directory.'''

        if self.venv:
            postactivate_file = os.path.join(self.venv.venv_path,
                                             'bin', 'postactivate')

            f = open(postactivate_file, 'w')
            f.write('#!/bin/bash\n')
            f.write('# This hook is run after this virtualenv is '
                    'activated.\n\n')
            f.write('cd %s\n' % self.template.project_root)
            f.close()
