# -*- coding: utf-8 -*-

"""
.. module:: facio.start
   :synopsis: Process the users template using Jninja2 rendering it
              out into the current working directory.
"""

import fnmatch
import os
import re
import shutil

from codecs import open
from facio.base import BaseFacio
from facio.exceptions import FacioException
from facio.state import state
from facio.vcs import GitVCS, MercurialVCS

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:  # pragma: no cover
    raise FacioException('Jinja2 must be installed to use Facio')


# Regex for extracting context variable name from file or directory name
get_var_name_pattern = re.compile(r'\{\{(\w+)\}\}')


class Template(BaseFacio):

    COPY_ATTEMPT_LIMIT = 5
    COPY_ATTEMPT = 1

    def __init__(self, origin):
        """ Constructor for Template Class sets the project template origin.
        It also sets the default ignore globs.

        :param origin: The origin path to the template
        :type origin: str
        """

        self.origin = origin

        # Update copy ignore globs with standard ignore patterns
        self.update_copy_ignore_globs([
            '.git',
            '.hg',
            '.svn',
            '.DS_Store',
            'Thumbs.db',
        ])

        # Update render ignore globs
        self.update_render_ignore_globs([
            '*.png',
            '*.gif',
            '*.jpeg',
            '*.jpg',
        ])

    def update_copy_ignore_globs(self, globs):
        """ Update the ignore glob patterns to include the list provided.

        ** Usage: **

        .. code-block:: python

            from facio.template import Template
            t = Template('foo', '/path/to/foo')
            globs = [
                '*.png',
                '*.gif',
            ]
            t.update_copy_ignore_globs(globs)

        :param globs: A list of globs
        :type globs: list
        """

        try:
            self.copy_ignore_globs += globs
        except AttributeError:
            if not isinstance(globs, list):
                self.copy_ignore_globs = []
            else:
                self.copy_ignore_globs = globs
        except TypeError:
            raise FacioException('Failed to add {0} to ignore globs '
                                 'list'.format(globs))

    def get_copy_ignore_globs(self):
        """ Returns ignore globs list at time of call.

        :returns: list
        """

        try:
            return self.copy_ignore_globs
        except AttributeError:
            return []

    def update_render_ignore_globs(self, globs):
        """ Update the render ignore glob patterns to include the
        list provided.

        ** Usage: **

        .. code-block:: python

            from facio.template import Template
            t = Template('foo', '/path/to/foo')
            globs = [
                '*.png',
                '*.gif',
            ]
            t.update_render_ignore_globs(globs)

        :param globs: A list of globs
        :type globs: list
        """

        try:
            self.render_ignore_globs += globs
        except AttributeError:
            if not isinstance(globs, list):
                self.render_ignore_globs = []
            else:
                self.render_ignore_globs = globs
        except TypeError:
            raise FacioException('Failed to add {0} to ignore globs '
                                 'list'.format(globs))

    def get_render_ignore_globs(self):
        """ Returns ignore globs list at time of call.

        :returns: list
        """

        try:
            return self.render_ignore_globs
        except AttributeError:
            return []

    def get_render_ignore_files(self, files):
        """ Returns a list of files to ignore for rendering based on
        ``get_render_ignore_globs`` patterns.

        :param files: List of files to check against
        :type files: list

        :returns: list -- list of filenames
        """

        ignores = []
        for pattern in self.get_render_ignore_globs():
            for filename in fnmatch.filter(files, pattern):
                ignores.append(filename)

        return ignores

    def copy(self, callback=None):
        """ Copy template from origin path to ``state.get_project_root()``.

        :param callback: A callback function to be called after
                         copy is complete
        :type callback: function -- default None

        :returns: bool
        """

        self.out('Copying {0} to {1}'.format(
            self.origin,
            state.get_project_root()))

        ignore = shutil.ignore_patterns(*self.get_copy_ignore_globs())
        try:
            shutil.copytree(self.origin, state.get_project_root(),
                            ignore=ignore)
        except shutil.Error:
            raise FacioException('Failed to copy {0} to {1}'.format(
                self.origin,
                state.get_project_root()))
        except OSError:
            # If we get an OSError either the template path does not exist or
            # the project root already exists. Check the later first and then
            # check if the template path is git+ or hg+ and clone, finally
            # raising exceptions

            if not os.path.isdir(state.get_project_root()):

                supported_vcs = [
                    ('git+', GitVCS),
                    ('hg+', MercurialVCS),
                ]

                for prefix, cls in supported_vcs:
                    if self.origin.startswith(prefix):
                        vcs = cls(self.origin)
                        new_path = vcs.clone()
                        if not new_path:
                            raise FacioException(
                                'New path to template not returned by '
                                '{0}.clone()'.format(vcs.__class__.__name__))
                        self.origin = new_path
                        break
                else:
                    # Loop feel through so path is not prefixed with git+ or
                    # +hg so it must be a path that does not exist
                    raise FacioException('{0} does not exist'.format(
                        self.origin))

                # The loop broke so we can call self.copy again
                if self.COPY_ATTEMPT <= self.COPY_ATTEMPT_LIMIT:
                    self.COPY_ATTEMPT += 1
                    self.copy(callback=vcs.remove_tmp_dir)
                else:
                    raise FacioException('Failed to copy template after '
                                         '{0} attempts'.format(
                                             self.COPY_ATTEMPT))

            else:
                # project root exists, raise exception
                raise FacioException('{0} already exists'.format(
                    state.get_project_root()))

        # Call callback if callable
        if callable(callback):
            callback(
                origin=self.origin,
                destination=state.get_project_root())

        return True

    def rename_direcories(self):
        """ Renames directories that are named after context variables, for
        example: ``{{PROJECT_NAME}}``.

        :returns: generator
        """

        for root, dirs, files in os.walk(state.get_project_root()):
            for directory in fnmatch.filter(dirs, '*{{*}}*'):
                var_name = get_var_name_pattern.findall(directory)[0]
                var_value = state.get_context_variable(var_name)
                if var_value:
                    old_path = os.path.join(root, directory)
                    new_path = os.path.join(root, var_value)
                    shutil.move(old_path, new_path)
                    yield (old_path, new_path)

    def rename_files(self):
        """ Rename files that are named after context variables, for example:
        ``{{PROJECT_NAME}}.py``

        :returns: generator
        """

        for root, dirs, files in os.walk(state.get_project_root()):
            for filename in fnmatch.filter(files, '*{{*}}*'):
                var_name = get_var_name_pattern.findall(filename)[0]
                var_value = state.get_context_variable(var_name)
                if var_value:
                    name, ext = os.path.splitext(filename)
                    old_path = os.path.join(root, filename)
                    new_path = os.path.join(root, '{0}{1}'.format(
                        var_value, ext))
                    shutil.move(old_path, new_path)
                    yield (old_path, new_path)

    def rename(self):
        """ Runs the two rename files and rename directories methods. """

        for old, new in self.rename_direcories():
            self.out('Renaming {0} to {1}'.format(old, new))

        for old, new in self.rename_files():
            self.out('Renaming {0} to {1}'.format(old, new))

    def render(self):
        """ Reads the template and uses Jinja 2 to replace context variables
        with their real values.
        """

        variables = state.get_context_variables()
        for root, dirs, files in os.walk(state.get_project_root()):
            jinja_loader = FileSystemLoader(root)
            jinja_environment = Environment(loader=jinja_loader)
            ignores = self.get_render_ignore_files(files)
            for filename in files:
                if filename not in ignores:
                    path = os.path.join(root, filename)
                    try:
                        template = jinja_environment.get_template(filename)
                        rendered = template.render(variables)
                    except:
                        import sys
                        e = sys.exc_info()[1]
                        self.warning('Failed to render {0}: {1}'.format(
                            path, e))
                    else:
                        with open(path, 'w', encoding='utf8') as handler:
                            handler.write(rendered)
