# -*- coding: utf-8 -*-

"""
.. module:: tests.test_pipeline.test_python
   :synopsis: Tests for bundled python pipelines
"""

from mock import patch, PropertyMock

from .. import BaseTestCase


class TestPythonVirtualenv(BaseTestCase):

    def setUp(self):
        # Mocking State
        patcher = patch('facio.pipeline.python.virtualenv.state',
                        new_callable=PropertyMock,
                        create=True)
        self.mock_state = patcher.start()
        self.mock_state.project_name = 'foo'
        self.mock_state.context_variables = {
            'PROJECT_NAME': 'foo'}
        self.addCleanup(patcher.stop)
