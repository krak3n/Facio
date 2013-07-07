# -*- coding: utf-8 -*-

"""
.. module:: facio.start
   :synopsis: Starts the Facio template process.
"""

import os

from facio.base import BaseFacio
from facio.config import Settings, CommandLineInterface, ConfigurationFile
from facio.template import Template
from facio.pipeline import Pipeline


class Start(BaseFacio):

    def start(self):

        interface = CommandLineInterface()
        interface.start()

        config = ConfigurationFile()
        parsed = config.read()

        settings = Settings(interface, parsed)

        template = Template(
            settings.get_project_name(),
            settings.get_template_path()
        )

        template.update_context_variables(settings.get_variables())
        template.update_ignore_globs(settings.get_ignore_globs())

        template.copy()

        pipeline = Pipeline()
        pipeline.load(os.path.join(
            template.get_project_root(),
            '.facio.pipeline.yml'
        ))

        if pipeline.has_before():
            pipeline.run_before()

        template.rename()
        template.write()

        if pipeline.has_after():
            pipeline.run_after()

        self.success('Done')
