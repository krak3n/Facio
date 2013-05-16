"""
facio.vcs.git_vcs
-----------------

Git Version Control Template Cloning.
"""

import os
import tempfile

from clint.textui import puts, indent
from clint.textui.colored import blue
from shutil import rmtree


class Git(object):

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
        tmp_dir = tempfile.mkdtemp(suffix='facio')

        try:
            from git import Repo
        except ImportError:
            raise Exception  # TODO: Custom exception

        try:
            repo = Repo.init(self.tmp_dir)
            repo.create_remote('origin', self.repo)
            origin = repo.remotes.origin
            origin.fetch()
            origin.pull('master')  # TODO: Branch prompt to the user
        except Exception:
            raise Exception  # TODO: Custom exception

        rmtree(os.path.join(tmp_dir, '.git'))

        with indent(4, quote=' >'):
            puts(blue('Clone complete'))
