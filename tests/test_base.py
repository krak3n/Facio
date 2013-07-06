# -*- coding: utf-8 -*-

"""
.. module:: tests.test_base
   :synopsis: Tests for Facio base class
"""

from facio.base import Facio

from . import BaseTestCase


class TestFacio(BaseTestCase):

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
        ])

    def test_out(self):
        f = Facio()
        f.out('Foo')

        self.mocked_facio_base_puts.called_once_with('Foo')

    def test_warning(self):
        f = Facio()
        f.warning('Foo')

        self.mocked_facio_base_puts.called_once_with('Warning: Foo')

    def test_error(self):
        f = Facio()
        f.error('Foo')

        self.mocked_facio_base_puts.called_once_with('Error: Foo')

    def test_success(self):
        f = Facio()
        f.success('Foo')

        self.mocked_facio_base_puts.called_once_with('Success: Foo')
