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

    @patch('facio.pipeline.import_module', return_value=True)
    def test_import_success(self, mock_importlib):
        p = Pipeline(self.template)
        with patch('facio.pipeline.puts') as puts:
            p.import_module('path.to.module')
            puts.assert_called_with('Loaded module: path.to.module')

    def test_import_module_failure(self):
        p = Pipeline(self.template)
        with patch('facio.pipeline.puts') as puts:
            p.import_module('pipeline_test_module')
            puts.assert_called_with('Failed to Load module: '
                                    'pipeline_test_module')

    def test_run_module_success(self):
        p = Pipeline(self.template)
        module = MagicMock()
        module.run.return_value = True
        rtn = p.run_module(module)
        self.assertTrue(module.run.called)
        self.assertTrue(rtn)

    def test_run_module_failure(self):
        p = Pipeline(self.template)
        module = MagicMock()
        module.run.side_effect = AttributeError
        rtn = p.run_module(module)
        self.assertTrue(module.run.called)
        self.assertFalse(rtn)

    def test_module_exception_caught(self):
        module = MagicMock()
        module.foo.side_effect = KeyError('Failed lookup')

        def fake_run():
            module.foo()

        module.run = fake_run
        p = Pipeline(self.template)
        with patch('facio.pipeline.puts') as puts:
            p.run_module(module)
        self.assertTrue(module.foo.called)
        puts.assert_called_with('Exeption caught in module: '
                                '\'Failed lookup\' line: 84')
