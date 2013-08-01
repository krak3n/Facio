# -*- coding: utf-8 -*-

"""
.. module:: facio.run
   :synopsis: Runs the Facio template process.
"""

import os

from facio.base import BaseFacio
from facio.config import (HOOKS_FILE_NAME,
                          Settings,
                          CommandLineInterface,
                          ConfigurationFile)
from facio.hooks import Hook
from facio.template import Template
from facio.state import state


class Run(BaseFacio):

    def run(self):
        """ Run the Facio processes. """

        interface = CommandLineInterface()
        interface.start()

        config = ConfigurationFile()
        parsed = config.read()

        settings = Settings(interface, parsed)
        state.update_context_variables(settings.get_variables())

        template = Template(settings.get_template_path())
        template.update_copy_ignore_globs(settings.copy_ignore_globs())
        template.update_render_ignore_globs(settings.render_ignore_globs())
        template.copy()

        pipeline = Hook()
        pipeline.load(os.path.join(
            state.get_project_root(),
            HOOKS_FILE_NAME))

        if pipeline.has_before():
            pipeline.run_before()

        template.rename()
        template.render()

        if pipeline.has_after():
            pipeline.run_after()

        self.success('Done')
