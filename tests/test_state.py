# -*- coding: utf-8 -*-

"""
.. module:: tests.state
   :synopsis: Tests for facios state module
"""

from facio.state import State
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

    def test_same_instance_always_returned(self):
        s1 = State()
        s2 = State()

        self.assertEqual(s1.state, s2.state)

    def test_get_set_project_name(self):
        state = State()
        state.set_project_name('foo')

        self.assertEqual(state.get_project_name(), 'foo')
