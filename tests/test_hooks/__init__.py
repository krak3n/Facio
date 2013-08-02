# -*- coding: utf-8 -*-

"""
.. module:: tests.test_hooks
   :synopsis: Tests for the facio hooks module.
"""

from facio.hooks import Hook
from mock import MagicMock, mock_open, patch
from random import choice

from .. import BaseTestCase


class HookTest(BaseTestCase):
    """ hooks Tests """

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
            'facio.hooks.Hook.out',
            'facio.hooks.Hook.warning',
            'facio.hooks.Hook.error',
        ])

    def _mock_open(self, data):
        patcher = patch('facio.hooks.open',
                        mock_open(read_data=data),
                        create=True)
        return patcher

    def _module_factory(self, n):
        """ Generate n number of mocked hooks modules.

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

        i = Hook()
        i.load('/foo/bar.yml')
        self.mocked_facio_hooks_Hook_out.assert_called_with(
            'Loading hooks')

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

        i = Hook()
        i.load('/foo/bar.yml')
        self.mocked_facio_hooks_Hook_warning.assert_called_with(
            "Error loading /foo/bar.yml hooks - Is it correctly formatted?")
        open_mock.stop()

    def test_load_ioerror(self):
        open_mock = self._mock_open('')
        m = open_mock.start()
        m.side_effect = IOError

        i = Hook()
        i.load('/foo/bar.yml')

        self.mocked_facio_hooks_Hook_warning.assert_called_with(
            "/foo/bar.yml not found")
        self.assertFalse(i._validate_before())
        self.assertFalse(i._validate_after())

        open_mock.stop()

    def test_yaml_formatted_correctly_before(self):
        data = """
        before:
            foo:
                - thing.bar
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        i = Hook()
        i.load('/foo/bar.yml')
        self.assertFalse(i.has_before())
        self.mocked_facio_hooks_Hook_warning.assert_called_with(
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

        i = Hook()
        i.load('/foo/bar.yml')
        self.assertFalse(i.has_after())
        self.mocked_facio_hooks_Hook_warning.assert_called_with(
            'Ignoring after: should be a list')

        open_mock.stop()

    def test_empty_hooks_always_retuns_false(self):
        data = """
        """
        open_mock = self._mock_open(data)
        open_mock.start()
        i = Hook()
        i.load('/foo/bar.yml')

        self.assertFalse(i.has_before())
        self.assertFalse(i.has_after())
        open_mock.stop()

    def test_has_before_true(self):
        data = """
        before:
            - thing.foo.bar
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        i = Hook()
        i.load('/foo/bar.yml')
        self.assertTrue(i.has_before())

        open_mock.stop()

    def test_has_before_false(self):
        data = """
        not_before:
            - thing.foo.bar
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        i = Hook()
        i.load('/foo/bar.yml')
        self.assertFalse(i.has_before())

        open_mock.stop()

    def test_has_after_true(self):
        data = """
        after:
            - thing.foo.bar
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        i = Hook()
        i.load('/foo/bar.yml')
        self.assertTrue(i.has_after())

        open_mock.stop()

    def test_has_after_false(self):
        data = """
        not_after:
            - thing.foo.bar
        """
        open_mock = self._mock_open(data)
        open_mock.start()

        i = Hook()
        i.load('/foo/bar.yml')
        self.assertFalse(i.has_after())

        open_mock.stop()

    @patch('facio.hooks.Hook.load', return_value=True)
    @patch('facio.hooks.import_module', return_value=True)
    def test_import_success(self, mock_importlib, mockload):
        i = Hook()
        i.load('/foo/bar.yml')
        i.import_module('path.to.module')
        self.mocked_facio_hooks_Hook_out.assert_called_with(
            'Loaded module: path.to.module')

    @patch('facio.hooks.Hook.load', return_value=True)
    def test_import_module_failure(self, mockload):
        i = Hook()
        i.load('/foo/bar.yml')
        i.import_module('hooks_test_module')

        self.mocked_facio_hooks_Hook_error.assert_called_with(
            'Failed to Load module: hooks_test_module')

    @patch('facio.hooks.Hook.load', return_value=True)
    def test_run_module_success(self, mockload):
        i = Hook()
        i.load('/foo/bar.yml')
        import_module_mock = patch('facio.hooks.Hook.import_module')
        mock = import_module_mock.start()
        module = MagicMock()
        module.run.return_value = True
        mock.return_value = module
        rtn = i.run_module('foo.bar.baz')
        mock = import_module_mock.stop()
        self.assertTrue(module.run.called)
        self.assertTrue(rtn)

    @patch('facio.hooks.Hook.load', return_value=True)
    def test_run_module_failure(self, mockload):
        i = Hook()
        i.load('/foo/bar.yml')
        import_module_mock = patch('facio.hooks.Hook.import_module')
        mock = import_module_mock.start()
        module = MagicMock()
        module.run.side_effect = AttributeError
        mock.return_value = module
        rtn = i.run_module('foo.bar.baz')
        mock = import_module_mock.stop()
        self.assertTrue(module.run.called)
        self.assertFalse(rtn)

    @patch('facio.hooks.Hook.load', return_value=True)
    def test_module_exception_caught(self, mockload):
        import_module_mock = patch('facio.hooks.Hook.import_module')
        mock = import_module_mock.start()
        module = MagicMock()
        module.foo.side_effect = KeyError('Failed lookup')
        mock.return_value = module

        def fake_run():
            module.foo()

        module.run = fake_run
        i = Hook()
        i.load('/foo/bar.yml')
        i.run_module('foo.bar.baz')
        mock = import_module_mock.stop()
        self.assertTrue(module.foo.called)
        self.mocked_facio_hooks_Hook_warning.assert_called_with(
            'Exeption caught in module: \'Failed lookup\' line: 117')

    @patch('facio.hooks.Hook.load', return_value=True)
    def test_store_hooks_states(self, return_value=True):
        i = Hook()
        i.load('/foo/bar.yml')
        import_module_mock = patch('facio.hooks.Hook.import_module')
        mock_import = import_module_mock.start()
        mocked_modules = self._module_factory(3)

        for path, module in mocked_modules:
            mock_import.return_value = module
            i.run_module(path)

            self.assertTrue(module.run.called)
            self.assertEqual(i.calls[-1:][0].get(path),
                             module.run.return_value)

        mock_import = import_module_mock.stop()

        self.assertEquals(len(i.calls), 3)

    @patch('facio.hooks.Hook.load', return_value=True)
    def test_hooks_call_history_retrival(self, return_value=True):
        i = Hook()
        i.load('/foo/bar.yml')
        import_module_mock = patch('facio.hooks.Hook.import_module')
        mock_import = import_module_mock.start()
        mocked_modules = self._module_factory(10)
        for path, module in mocked_modules:
            mock_import.return_value = module
            i.run_module(path)
        import_module_mock.stop()

        self.assertFalse(i.has_run('not.in.facked.modules'))
        self.assertEqual(i.has_run('foo.bar.baz2'), mocked_modules[1][1].run())

    def test_run_before(self):
        data = """
        before:
            - thing.foo.bar
        """
        import_module_mock = patch('facio.hooks.Hook.import_module')
        mock_import = import_module_mock.start()
        mock_module = MagicMock()
        mock_module.run.return_value = True
        mock_import.return_value = mock_module
        open_mock = self._mock_open(data)
        open_mock.start()

        i = Hook()
        i.load('/foo/bar.yml')
        i.run_before()

        open_mock.stop()

        self.assertTrue(mock_module.run.called)
        self.assertTrue(i.has_run('thing.foo.bar'))

    def test_run_after(self):
        data = """
        after:
            - thing.foo.bar
        """
        import_module_mock = patch('facio.hooks.import_module')
        mock_import = import_module_mock.start()
        mock_module = MagicMock()
        mock_module.run.return_value = True
        mock_import.return_value = mock_module
        open_mock = self._mock_open(data)
        open_mock.start()

        i = Hook()
        i.load('/foo/bar.yml')
        i.run_after()

        self.assertTrue(mock_module.run.called)
        self.assertTrue(i.has_run('thing.foo.bar'))

        open_mock.stop()
