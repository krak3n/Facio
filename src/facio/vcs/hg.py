# -*- coding: utf-8 -*-

"""
.. module:: facio.vcs.hg
   :synopsis: Mercurial repository template cloning.
"""

import os
import tempfile

from clint.textui import puts, indent
from clint.textui.colored import blue
from shutil import rmtree


class Mercurial(object):

    tmp_dir = None

    def __init__(self, template_path):
        self.template_path = template_path
        with indent(4, quote=' >'):
            puts(blue('Cloning template using Mercurial from: {0}'.format(
                self.repo)))

    @property
    def repo(self):
        if not hasattr(self, '_repo'):
            self._repo = self.template_path.replace('hg+', '')
        return self._repo

    def clone(self):
        try:
            from sh import hg
        except ImportError:
            # TODO: Custom exception
            raise ImportError('Please install Mercurial')

        self.tmp_dir = tempfile.mkdtemp(suffix='facio')

        try:
            hg = hg.bake(_cwd=self.tmp_dir)
            hg.clone(self.repo, self.tmp_dir)
        except Exception:
            raise Exception  # TODO: Custom exception

        rmtree(os.path.join(self.tmp_dir, '.hg'))

        with indent(4, quote=' >'):
            puts(blue('Clone complete'))
