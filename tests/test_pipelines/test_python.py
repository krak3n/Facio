# -*- coding: utf-8 -*-

"""
.. module:: tests.test_pipeline.test_python
   :synopsis: Tests for bundled python pipelines
"""

from facio.pipeline.python.virtualenv import Virtualenv
from mock import patch, PropertyMock

from .. import BaseTestCase


class TestPythonVirtualenv(BaseTestCase):

    def setUp(self):
        # Mocking State
        patcher = patch('facio.state.state.state',
                        new_callable=PropertyMock,
                        create=True)
        self.mock_state = patcher.start()
        self.mock_state.project_name = 'foo'
        self.mock_state.context_variables = {
            'PROJECT_NAME': 'foo'}
        self.addCleanup(patcher.stop)

    @patch('facio.base.input')
    def test_get_name(self, mock_input):
        mock_input.return_value = 'bar'

        i = Virtualenv()
        name = i.get_name()

        self.assertEqual(name, 'bar')

    @patch('facio.base.input')
    def test_get_name_default(self, mock_input):
        mock_input.return_value = ''

        i = Virtualenv()
        name = i.get_name()

        self.assertEqual(name, 'foo')
