"""
facio.__init__
--------------

This kicks the whole thing off, fireing CLI option prompt and processing
the template.
"""

__version__ = '1.1.1'


class Facio(object):

    def __init__(self):
        '''Constructor, fires all required methods.'''

        from .config import Config
        from .template import Template

        from clint.textui import puts, indent
        from clint.textui.colored import green

        # Basic Skeleton Generation
        self.config = Config()

        with indent(4, quote=' >'):
            puts(green('Starting'))

        self.template = Template(self.config)
        self.template.copy_template()

        with indent(4, quote=' >'):
            puts(green('Done'))
