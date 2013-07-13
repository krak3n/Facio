# -*- coding: utf-8 -*-

"""
.. module:: tests.test_pipeline.test_django
   :synopsis: Tests for bundled django pipelines
"""


from facio.pipeline.django.secret_key import GenerateDjangoSecretKey, run
from facio.state import state
from mock import patch
from six.moves import builtins

from .. import BaseTestCase


class TestDjangoSecretKey(BaseTestCase):

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
            'facio.pipeline.django.secret_key.GenerateDjangoSecretKey.out',
        ])

    def tearDown(self):
        try:
            del(builtins.__facio__)
        except AttributeError:
            pass

    @patch('facio.pipeline.django.secret_key.choice', create=True)
    @patch('facio.pipeline.django.secret_key.range', create=True)
    def test_generate_key(self, mock_range, mock_choice):
        mock_range.return_value = [0, ]
        mock_choice.return_value = 'a'

        i = GenerateDjangoSecretKey()
        key = i.generate()

        self.assertEqual(key, 'a')
        self.mocked_facio_pipeline_django_secret_key_GenerateDjangoSecretKey_out.assert_called_with('Generating Django Secret Key')  # NOQA

    @patch('facio.pipeline.django.secret_key.GenerateDjangoSecretKey.generate')
    def test_run(self, mock_generate):
        mock_generate.return_value = 'foobarbaz'

        key = run()

        self.assertEqual(key, 'foobarbaz')
        self.assertEqual(state.context_variables['DJANGO_SECRET_KEY'],
                         'foobarbaz')
