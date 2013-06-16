"""
.. module:: tests.test_pipeline
   :synopsis: Tests for the facio pipeline module.
"""

import os

from facio.pipeline import Pipeline
from mock import MagicMock, patch

from .base import BaseTestCase


class PipelineTest(BaseTestCase):
    """ Pipeline Tests """

    def setUp(self):
        self.template = self._mock_template_class()

    def _mock_template_class(self):
        template = MagicMock(name='template')
        template.pipeline_file = os.path.join(
            self.test_pieplines_path,
            'complete.yml')
        template.config = MagicMock(name='config')

        return template

    def test_can_load_yaml(self):
        with patch('facio.pipeline.puts') as puts:
            Pipeline(self.template)
            puts.assert_called_with("Loading Pipeline")

    def test_yaml_load_error_output(self):
        self.template.pipeline_file = os.path.join(
            self.test_pieplines_path,
            'malformed.yml')
        with patch('facio.pipeline.puts') as puts:
            Pipeline(self.template)
        puts.assert_called_with("Error loading Pipeline - Is it correctly "
                                "formatted?")

    def test_empty_pipeline_always_retuns_false(self):
        self.template.pipeline_file = os.path.join(
            self.test_pieplines_path,
            'empty.yml')
        p = Pipeline(self.template)

        self.assertFalse(p.has_before)
        self.assertFalse(p.has_after)

    def test_has_before_true(self):
        p = Pipeline(self.template)
        self.assertTrue(p.has_before)

    def test_has_before_false(self):
        self.template.pipeline_file = os.path.join(
            self.test_pieplines_path,
            'after.yml')
        p = Pipeline(self.template)
        self.assertFalse(p.has_before)

    def test_has_after_true(self):
        p = Pipeline(self.template)
        self.assertTrue(p.has_after)

    def test_has_after_false(self):
        self.template.pipeline_file = os.path.join(
            self.test_pieplines_path,
            'before.yml')
        p = Pipeline(self.template)
        self.assertFalse(p.has_after)

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
