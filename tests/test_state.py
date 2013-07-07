# -*- coding: utf-8 -*-

"""
.. module:: tests.state
   :synopsis: Tests for facios state module
"""

from . import BaseTestCase


class TestState(BaseTestCase):

    def test_same_instance_always_returned(self):
        from facio.state import state as s1
        from facio.state import state as s2
        from facio.state import State

        s3 = State()

        self.assertEqual(s1, s2)
        self.assertEqual(s1, s2.state)
        self.assertNotEqual(s1, s3)
        self.assertEqual(s1, s3.state)

    def test_get_set_project_name(self):
        from facio.state import state as s1
        from facio.state import state as s2

        s1.set_project_name('foo')

        self.assertEqual(s2.get_project_name(), 'foo')
