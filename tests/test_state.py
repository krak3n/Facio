# -*- coding: utf-8 -*-

"""
.. module:: tests.state
   :synopsis: Tests for facios state module
"""

from facio.state import State
from mock import patch
from six.moves import builtins

from . import BaseTestCase


class TestState(BaseTestCase):

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
            'facio.exceptions.puts',
            'facio.state.State.warning',
        ])

    def tearDown(self):
        del(builtins.__facio__)

    def test_same_instance_always_returned(self):
        s1 = State()
        s2 = State()

        self.assertEqual(s1.state, s2.state)

    def test_get_set_project_name(self):
        state = State()
        state.set_project_name('foo')

        self.assertEqual(state.get_project_name(), 'foo')

    @patch('facio.state.pwd', return_value='/foo')
    def test_return_current_working_dir(self, mock_pwd):
        state = State()
        state.set_project_name('foo')

        self.assertEqual(state.get_working_directory(), '/foo')

    @patch('facio.state.pwd', return_value='/bar')
    def test_return_project_root(self, mock_pwd):
        state = State()
        state.set_project_name('foo')

        self.assertEqual(state.get_project_root(), '/bar/foo')

    def test_update_context_variables(self):
        state = State()

        state.update_context_variables([1, 2, 3])

        self.mocked_facio_state_State_warning.assert_called_once_with(
            'Failed to update context variables with [1, 2, 3]')

    def test_get_context_variables_empty(self):
        state = State()

        self.assertEqual(state.get_context_variables(), {})

    def test_get_context_variables(self):
        state = State()

        state.update_context_variables({'PROJECT_NAME': 'foo'})

        self.assertEqual(state.get_context_variables(), {
            'PROJECT_NAME': 'foo'})

    def test_get_context_variable(self):
        state = State()

        state.update_context_variables({'PROJECT_NAME': 'foo'})

        self.assertEqual(state.get_context_variable('PROJECT_NAME'), 'foo')
        self.assertNotEqual(state.get_context_variable('not_created'), 'foo')

    def test_pipeline_call_save(self):
        state = State()

        state.pipeline_save_call('foo.bar', 'baz')
        state.pipeline_save_call('baz.foo', 'bar')
        calls = state.pipeline_save_call('foo.bar', 'baz')

        self.assertEqual(calls, [('foo.bar', 'baz'), ('baz.foo', 'bar')])

    def test_pipeline_get_call(self):
        state = State()

        state.pipeline_save_call('foo.bar', 'baz')
        state.pipeline_save_call('baz.foo', 'bar')

        self.assertEqual(state.pipeline_get_call_result('foo.bar'), 'baz')
        self.assertEqual(state.pipeline_get_call_result('baz.foo'), 'bar')
