import optparse

from facio.opts import Option

from .base import BaseTestCase


class OptsTests(BaseTestCase):
    """ Option Tests. """

    def test_raise_exception_when_require_used_incorrectly(self):
        try:
            Option('-n', '--does_not_take_val', action="store_true",
                    default=None, required=True)
        except optparse.OptionError:
            assert True
