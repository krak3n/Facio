"""
.. module:: tests.test_vcs.git
   :synopsis: Unit tests for the git vcs module
"""

import os
import tempfile
import uuid

from facio.template import Template
from mock import MagicMock, PropertyMock, patch
from sh import git
from six import StringIO
from shutil import rmtree

from ..base import BaseTestCase


class HgTests(BaseTestCase):
    """ Mercurial Tests """

    def setUp(self):
        self.config = MagicMock(name='config')
        self.config.project_name = uuid.uuid4().hex  # Random project name
        self.config.django_secret_key = 'xxx'
        self.config.template_settings_dir = 'settings'
        self.config.cli_opts.error = MagicMock(side_effect=Exception)
        self.puts_patch = patch(
            'facio.template.puts',
            stream=StringIO)
        self.puts_patch.start()
        self.puts_patch_vcs = patch(
            'facio.vcs.hg.puts',
            stream=StringIO)
        self.puts_patch_vcs.start()
