# -*- coding: utf-8 -*-

"""
.. module:: tests.test_pipeline
   :synopsis: Tests for the facio pipeline module.
"""

import six

from facio.pipeline import Pipeline
from mock import MagicMock, mock_open, patch
from random import choice

from . import BaseTestCase


class PipelineTest(BaseTestCase):
    """ Pipeline Tests """

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
            'facio.pipeline.Pipeline.out',
            'facio.pipeline.Pipeline.warning',
            'facio.pipeline.Pipeline.error',
        ])

    def _mock_open(self, data):
        if six.PY3:
            func = 'builtins.open'
        else:
            func = '__builtin__.open'
        patcher = patch(
            func,
            mock_open(read_data=data),
            create=True)
        return patcher

    def _module_factory(self, n):
        """ Generate n number of mocked pipeline modules.

        :param n: Number of modules to generate
        :type n: int

        :returns: list -- List of mocked modules as tuples
        """

        modules = []
        for x in range(1, (n + 1)):
            mocked_module = MagicMock()
            mocked_module .run.return_value = n * choice(range(1, 11))
            modules.append((
                'foo.bar.baz{0}'.format(x),
                mocked_module))
        return modules

    def test_can_load_yaml(self):
        data = """
        before:
            - foo.bar.thing
        after:
            - bare.foo.thing
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        p = Pipeline()
        p.load('/foo/bar.yml')
        self.mocked_facio_pipeline_Pipeline_out.assert_called_with(
            'Loading Pipeline')

        open_mock.stop()

    def test_yaml_load_error_output(self):
        data = """
        s:
        is
        not*
        *correct
        - hello
            :world
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        p = Pipeline()
        p.load('/foo/bar.yml')
        self.mocked_facio_pipeline_Pipeline_warning.assert_called_with(
            "Error loading /foo/bar.yml pipeline - Is it correctly formatted?")
        open_mock.stop()

    def test_yaml_formatted_correctly_before(self):
        data = """
        before:
            foo:
                - thing.bar
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        p = Pipeline()
        p.load('/foo/bar.yml')
        self.assertFalse(p.has_before())
        self.mocked_facio_pipeline_Pipeline_warning.assert_called_with(
            'Ignoring before: should be a list')

        open_mock.stop()

    def test_yaml_formatted_correctly_after(self):
        data = """
        after:
            foo:
                - thing.bar
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        p = Pipeline()
        p.load('/foo/bar.yml')
        self.assertFalse(p.has_after())
        self.mocked_facio_pipeline_Pipeline_warning.assert_called_with(
            'Ignoring after: should be a list')

        open_mock.stop()

    def test_empty_pipeline_always_retuns_false(self):
        data = """
        """
        open_mock = self._mock_open(data)
        open_mock.start()
        p = Pipeline()
        p.load('/foo/bar.yml')

        self.assertFalse(p.has_before())
        self.assertFalse(p.has_after())
        open_mock.stop()

    def test_has_before_true(self):
        data = """
        before:
            - thing.foo.bar
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        p = Pipeline()
        p.load('/foo/bar.yml')
        self.assertTrue(p.has_before())

        open_mock.stop()

    def test_has_before_false(self):
        data = """
        not_before:
            - thing.foo.bar
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        p = Pipeline()
        p.load('/foo/bar.yml')
        self.assertFalse(p.has_before())

        open_mock.stop()

    def test_has_after_true(self):
        data = """
        after:
            - thing.foo.bar
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        p = Pipeline()
        p.load('/foo/bar.yml')
        self.assertTrue(p.has_after())

        open_mock.stop()

    def test_has_after_false(self):
        data = """
        not_after:
            - thing.foo.bar
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        p = Pipeline()
        p.load('/foo/bar.yml')
        self.assertFalse(p.has_after())

        open_mock.stop()

    @patch('facio.pipeline.Pipeline.load', return_value=True)
    @patch('facio.pipeline.import_module', return_value=True)
    def test_import_success(self, mock_importlib, mockload):
        p = Pipeline()
        p.load('/foo/bar.yml')
        p.import_module('path.to.module')
        self.mocked_facio_pipeline_Pipeline_out.assert_called_with(
            'Loaded module: path.to.module')

    @patch('facio.pipeline.Pipeline.load', return_value=True)
    def test_import_module_failure(self, mockload):
        p = Pipeline()
        p.load('/foo/bar.yml')
        p.import_module('pipeline_test_module')
        self.mocked_facio_pipeline_Pipeline_error.assert_called_with(
            'Failed to Load module: pipeline_test_module')

    @patch('facio.pipeline.Pipeline.load', return_value=True)
    def test_run_module_success(self, mockload):
        p = Pipeline()
        p.load('/foo/bar.yml')
        import_module_mock = patch('facio.pipeline.import_module')
        mock = import_module_mock.start()
        module = MagicMock()
        module.run.return_value = True
        mock.return_value = module
        rtn = p.run_module('foo.bar.baz')
        self.assertTrue(module.run.called)
        self.assertTrue(rtn)
        mock = import_module_mock.stop()

    @patch('facio.pipeline.Pipeline.load', return_value=True)
    def test_run_module_failure(self, mockload):
        p = Pipeline()
        p.load('/foo/bar.yml')
        import_module_mock = patch('facio.pipeline.import_module')
        mock = import_module_mock.start()
        module = MagicMock()
        module.run.side_effect = AttributeError
        mock.return_value = module
        rtn = p.run_module('foo.bar.baz')
        self.assertTrue(module.run.called)
        self.assertFalse(rtn)
        mock = import_module_mock.stop()

    @patch('facio.pipeline.Pipeline.load', return_value=True)
    def test_module_exception_caught(self, mockload):
        import_module_mock = patch('facio.pipeline.import_module')
        mock = import_module_mock.start()
        module = MagicMock()
        module.foo.side_effect = KeyError('Failed lookup')
        mock.return_value = module

        def fake_run():
            module.foo()

        module.run = fake_run
        p = Pipeline()
        p.load('/foo/bar.yml')
        p.run_module('foo.bar.baz')
        self.assertTrue(module.foo.called)
        self.mocked_facio_pipeline_Pipeline_warning.assert_called_with(
            'Exeption caught in module: \'Failed lookup\' line: 114')
        mock = import_module_mock.stop()

    @patch('facio.pipeline.Pipeline.load', return_value=True)
    def test_store_pipeline_states(self, return_value=True):
        p = Pipeline()
        p.load('/foo/bar.yml')
        import_module_mock = patch('facio.pipeline.import_module')
        mock_import = import_module_mock.start()
        mocked_modules = self._module_factory(3)

        for path, module in mocked_modules:
            mock_import.return_value = module
            p.run_module(path)

            self.assertTrue(module.run.called)
            self.assertEqual(p.calls[-1:][0].get(path),
                             module.run.return_value)

        self.assertEquals(len(p.calls), 3)

        mock_import = import_module_mock.stop()

    @patch('facio.pipeline.Pipeline.load', return_value=True)
    def test_pipeline_call_history_retrival(self, return_value=True):
        p = Pipeline()
        p.load('/foo/bar.yml')
        import_module_mock = patch('facio.pipeline.import_module')
        mock_import = import_module_mock.start()
        mocked_modules = self._module_factory(10)
        for path, module in mocked_modules:
            mock_import.return_value = module
            p.run_module(path)

        self.assertFalse(p.has_run('not.in.facked.modules'))
        self.assertEqual(p.has_run('foo.bar.baz2'), mocked_modules[1][1].run())

    def test_run_before(self):
        data = """
        before:
            - thing.foo.bar
        """
        import_module_mock = patch('facio.pipeline.import_module')
        mock_import = import_module_mock.start()
        mock_module = MagicMock()
        mock_module.run.return_value = True
        mock_import.return_value = mock_module
        open_mock = self._mock_open(data)
        open_mock.start()

        p = Pipeline()
        p.load('/foo/bar.yml')
        p.run_before()

        self.assertTrue(mock_module.run.called)
        self.assertTrue(p.has_run('thing.foo.bar'))

        open_mock.stop()

    def test_run_after(self):
        data = """
        after:
            - thing.foo.bar
        """
        import_module_mock = patch('facio.pipeline.import_module')
        mock_import = import_module_mock.start()
        mock_module = MagicMock()
        mock_module.run.return_value = True
        mock_import.return_value = mock_module
        open_mock = self._mock_open(data)
        open_mock.start()

        p = Pipeline()
        p.load('/foo/bar.yml')
        p.run_after()

        self.assertTrue(mock_module.run.called)
        self.assertTrue(p.has_run('thing.foo.bar'))

        open_mock.stop()
