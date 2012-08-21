import os
import sys
import unittest


class BaseTestCase(unittest.TestCase):

    test_tpl_path = os.path.join(os.path.dirname(__file__), 'test_template')

    def setUp(self):
        self._old_sys_argv = sys.argv
        sys.argv = [self._old_sys_argv[0].replace('nosetests', 'skeletor')]

    def tearDown(self):
        sys.argv = self._old_sys_argv
