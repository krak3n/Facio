"""
.. module:: tests
   :synopsis: Base test class.
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from mock import patch


class BaseTestCase(unittest.TestCase):

    def _patch_clint(self, paths=[]):
        """ Mock the clint.textui modules, clint_paths on self
        is required for this method to work. """

        def effect(self, text):
            return text

        self.patched_ColoredString = patch(
            'clint.textui.colored.ColoredString', side_effect=effect)
        self.mocked_ColoredString = self.patched_ColoredString.start()

        try:
            for x, path in enumerate(paths):
                name = path.replace('.', '_')
                p = patch(path)
                self.addCleanup(p.stop)
                setattr(self, 'patched_{0}'.format(name), p)
                patcher = getattr(self, 'patched_{0}'.format(name))
                setattr(self, 'mocked_{0}'.format(name), patcher.start())
        except AttributeError:
            pass
