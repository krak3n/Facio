# -*- coding: utf-8 -*-

"""
.. module:: tests.test_hooks.test_django
   :synopsis: Tests for bundled django hooks
"""


from facio.hooks.django.secret import GenerateDjangoSecretKey, run
from facio.state import state
from mock import patch
from six.moves import builtins

from .. import BaseTestCase


class TestDjangoSecretKey(BaseTestCase):

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
            'facio.hooks.django.secret.GenerateDjangoSecretKey.out',
        ])

    def tearDown(self):
        try:
            del(builtins.__facio__)
        except AttributeError:
            pass

    @patch('facio.hooks.django.secret.choice', create=True)
    @patch('facio.hooks.django.secret.range', create=True)
    def test_generate_key(self, mock_range, mock_choice):
        mock_range.return_value = [0, ]
        mock_choice.return_value = 'a'

        i = GenerateDjangoSecretKey()
        key = i.generate()
        out = self.mocked_facio_hooks_django_secret_GenerateDjangoSecretKey_out

        self.assertEqual(key, 'a')
        out.assert_called_with('Generating Django Secret Key')

    @patch('facio.hooks.django.secret.GenerateDjangoSecretKey.generate')
    def test_run(self, mock_generate):
        mock_generate.return_value = 'foobarbaz'

        key = run()

        self.assertEqual(key, 'foobarbaz')
        self.assertEqual(state.context_variables['DJANGO_SECRET_KEY'],
                         'foobarbaz')
