"""
facio.vcs.git
-------------

Git Version Control Template Cloning.
"""

import os
import tempfile

from clint.textui import puts, indent
from clint.textui.colored import blue
from shutil import rmtree


class Git(object):

    tmp_dir = None

    def __init__(self, template_path):
        self.template_path = template_path
        with indent(4, quote=' >'):
            puts(blue('Cloning template using Git from: {0}'.format(
                self.repo)))

    @property
    def repo(self):
        if not hasattr(self, '_repo'):
            self._repo = self.template_path.replace('git+', '')
        return self._repo

    def clone(self):
        self.tmp_dir = tempfile.mkdtemp(suffix='facio')

        try:
            from sh import git
        except ImportError:
            raise Exception  # TODO: Custom exception

        try:
            git = git.bake(_cwd=self.tmp_dir)
            git.clone(self.repo, self.tmp_dir)
            git.fetch('--all')
            git.checkout('master')  # TODO: Branch prompt to the user
        except Exception:
            raise Exception  # TODO: Custom exception

        rmtree(os.path.join(self.tmp_dir, '.git'))

        with indent(4, quote=' >'):
            puts(blue('Clone complete'))
