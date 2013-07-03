"""
facio.vcs.git
-------------

Git Version Control Template Cloning.
"""

import tempfile

from clint.textui import puts, indent
from clint.textui.colored import blue


class Git(object):

    tmp_dir = None

    def __init__(self, template_path):
        self.template_path = template_path

    @property
    def repo(self):
        if not hasattr(self, '_repo'):
            self._repo = self.template_path.replace('git+', '')
        return self._repo

    def clone(self):

        with indent(4, quote=' >'):
            puts(blue('Cloning template using Git from: {0}'.format(
                self.repo)))

        try:
            from sh import git
        except ImportError:
            raise ImportError('Please install Git')  # TODO: Custom exception

        self.tmp_dir = tempfile.mkdtemp(suffix='facio')

        try:
            git = git.bake(_cwd=self.tmp_dir)
            git.clone(self.repo, self.tmp_dir)
            git.fetch('--all')
            git.checkout('master')  # TODO: Branch prompt to the user
        except Exception:
            raise Exception  # TODO: Custom exception

        with indent(4, quote=' >'):
            puts(blue('Clone complete'))

        return self.tmp_dir
