"""
.. module:: tests.test_pipeline
   :synopsis: Tests for the facio pipeline module.
"""

import os

from mock import MagicMock, patch
from six import StringIO

from .base import BaseTestCase


class PipelineTest(BaseTestCase):
    """ Pipeline Tests """

    def setUp(self):
        self.template = self._mock_template_class()
        self.puts = self._mock_puts()

    def _mock_template_class(self):
        template = MagicMock(name='template')
        template.pipeline_file = os.path.join(
            self.test_pieplines_path,
            'complete.yml')
        template.config = MagicMock(name='config')

        return template

    def _mock_puts(self):
        puts = patch('facio.pipeline.puts', stream=StringIO)
        puts.start()

        return puts

    def test_can_load_yaml(self):
        pass

    def test_yaml_load_error_output(self):
        pass

    def test_has_before_true(self):
        pass

    def test_has_before_false(self):
        pass

    def test_has_after_true(self):
        pass

    def test_has_after_false(self):
        pass

    def test_parse_success(self):
        pass

    def test_parse_failure_output_error(self):
        pass

    def test_import_success(self):
        pass

    def test_import_module_failure(self):
        pass

    def test_run_module_failure(self):
        pass

    def test_run_module_success(self):
        pass
