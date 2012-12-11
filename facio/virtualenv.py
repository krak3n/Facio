"""
facio.virtualenv
----------------

This is experimental. This should create a python virtual environment for the
project.
"""

import os

from subprocess import Popen, PIPE, STDOUT


class Virtualenv(object):

    def __init__(self, config):
        '''Install a new virtual environment for the new project.'''

        self.config = config

        if self.check_virtualenv_installed():
            self.create_virtualenv()

    @property
    def venv_name(self):
        '''Build venv_name.'''
        prefix = getattr(self.config, 'venv_prefix', None)
        if not prefix:
            return self.config.project_name
        else:
            name = ''.join([prefix, self.config.project_name])
            return name

    @property
    def venv_path(self):
        '''Return path to new virtualenvironment.'''

        return os.path.join(self.config.venv_path, self.venv_name)

    def check_virtualenv_installed(self):
        '''Check virtualenv is installed.'''

        error_msg = 'Virtualenv does not appear to be installed on your '\
                    'system. Please install python-virtualenv to use '\
                    'this feature of facio.'
        try:
            import virtualenv
        except ImportError:
            self.config._error(error_msg)
            return False
        else:
            # Lets double check
            cmd = 'which virtualenv'
            p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
                      close_fds=True)
            output = p.stdout.read()
            if output == '':
                self.config._error(error_msg)
                return False
        return True

    def validate(self):
        '''Validate virtualenv creattion.'''

        path = self.config.venv_path
        full_path = self.venv_path

        if not os.path.exists(self.config.venv_path):
            self.config._error('Specififed virtual environment path '
                               'does not exist: %s' % path)

        if os.path.exists(self.venv_path):
            self.config._error('A virtual environment at %s '
                               'already exists' % full_path)

        return True

    def create_virtualenv(self):
        '''Create python virtualevironment.'''

        if self.validate():
            print 'Creating python virtual environment at %s ...' % (
                self.venv_path)
            cmd = 'cd %s && virtualenv %s' % (self.config.venv_path,
                                              self.venv_path)
            if not getattr(self.config, 'venv_use_site_packages', False):
                cmd += ' --no-site-packages'
            print 'Runing: ' + cmd

            os.system(cmd)
