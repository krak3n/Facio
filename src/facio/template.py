# -*- coding: utf-8 -*-

"""
.. module:: facio.start
   :synopsis: Process the users template using Jninja2 rendering it
              out into the current working directory.
"""

import fnmatch
import glob
import os
import re
import shutil

from clint.textui import puts, indent
from clint.textui.colored import blue, yellow
from codecs import open
from sh import pwd

from .exceptions import FacioException
from .pipeline import Pipeline
from .vcs.git import Git
from .vcs.hg import Mercurial


# Regex for extracting context variable name from file or directory name
get_var_name_pattern = re.compile(r'\{\{(\w+)\}\}')


class Template(object):

    def __init__(self, name, path):
        """ Constructor for Template Class, sets the project name, template
        path, and takes several key word arguments.

        :param name: The project name
        :type name: str

        :param path: The path to the template
        :type path: str
        """

        self.name = name
        self.path = path

        # Update context variables to contain PROJECT_NAME
        self.update_context_variables([
            ('PROJECT_NAME', name)
        ])

        # Update ignore globs with standard ignore patterns
        self.update_ignore_globs([
            '.git',
            '.hg',
            '.svn',
            '*.pyc',
        ])

    def out(self, message, color=blue):
        """ Print message out to user using clint.

        :param message: Message to print to user
        :type message: str

        ** Optional Key Word Arguments **

        :param color: Clint color function to use
        :type: function -- default blue
        """

        with indent(4, quote=' >'):
            puts(color(message))

    def get_working_directory(self):
        """ Use the ``sh`` library to return the current working directory
        using the unix command ``pwd``.

        :returns: str
        """

        return '{0}'.format(pwd()).strip()

    def get_project_root(self):
        """ Return the project root, which is the current working directory
        plus the project name.

        :returns: str
        """

        return os.path.join(self.get_working_directory(), self.name)

    def update_context_variables(self, var_list):
        """ Update the context varaibles list with new key value tuple
        pairs.

        ** Usage: **

        .. code-block:: python

            from facio.template import Template
            var_list = [
                ('bar': 'baz'),
                ('fib': 'fab'),
            ]
            t = Template('foo', '/path/to/foo')
            t.update_context_variables(var_list)

        :param var_list: list of key value tuples
        :type var_list: list
        """

        try:
            self.context_variables += var_list
        except AttributeError:
            if not isinstance(var_list, list):
                var_list = []
            self.context_variables = var_list
        except TypeError:
            raise FacioException('Failed to add {0} to variables '
                                 'list'.format(var_list))

    def get_context_variables(self):
        """ Returns the current context variables at time of call.

        :retutns: list
        """

        try:
            return self.context_variables
        except AttributeError:
            return []

    def get_context_varable(self, name):
        """ Return a specific context variable value.

        :param name: Context variable name
        :type name: str

        :returns: str or None -- None if name not found in var list
        """

        variables = self.get_context_variables()
        try:
            name, value = filter(lambda t: t[0] == name, variables)[0]
            return value
        except IndexError:
            return None

    def update_ignore_globs(self, ignore_list):
        """ Update the ignore glob patterns to include the list provided.

        ** Usage: **

        .. code-block:: python

            from facio.template import Template
            t = Template('foo', '/path/to/foo')
            globs = [
                '*.png',
                '*.gif',
            ]
            t.update_ignore_globs(globs)

        :param ignore_list: A list of globs
        :type ignore_list: list
        """

        try:
            self.ignore_globs += ignore_list
        except AttributeError:
            if not isinstance(ignore_list, list):
                self.ignore_globs = []
            self.ignore_globs = ignore_list
        except TypeError:
            raise FacioException('Failed to add {0} to ignore globs '
                                 'list'.format(ignore_list))

    def get_ignore_globs(self):
        """ Returns ignore globs list at time of call.

        :returns: list
        """

        try:
            return self.ignore_globs
        except AttributeError:
            return []

    def copy(self):
        """ Copy template from origin path to ``self.get_project_root()``.

        :returns: bool
        """

        self.out('Copying {0} to {1}'.format(
            self.path,
            self.get_project_root()))

        ignore = shutil.ignore_patterns(*self.get_ignore_globs())
        try:
            shutil.copytree(self.path, self.get_project_root(), ignore=ignore)
        except shutil.Error:
            raise FacioException('Failed to copy {0} to {1}'.format(
                self.path,
                self.get_project_root()))
        except OSError:
            # If we get an OSError either the template path does not exist or
            # the project root already exists. Check the later first and then
            # check if the template path is git+ or hg+ and clone, finally
            # raising exceptions

            if not os.path.isdir(self.get_project_root()):

                supported_vcs = [
                    ('git+', Git),
                    ('hg+', Mercurial),
                ]

                for prefix, cls in supported_vcs:
                    if self.path.startswith(prefix):
                        vcs = cls(self.path)
                        self.path = vcs.clone()
                        break
                else:
                    # Loop feel through so path is not prefixed with git+ or
                    # +hg so it must be a path that does not exist
                    raise FacioException('{0} does not exist'.format(
                        self.path))

                # The loop broke so we can call self.copy again
                self.copy()

            else:
                # project root exists, raise exception
                raise FacioException('{0} already exists'.format(
                    self.get_project_root()))

        return True

    def rename_direcories(self):
        """ Renames directories that are named after context variables, for
        example: ``{{PROJECT_NAME}}``.

        :returns: generator
        """

        for root, dirs, files in os.walk(self.get_project_root()):
            for directory in fnmatch.filter(dirs, '*{{*}}*'):
                try:
                    var_name = get_var_name_pattern.findall(directory)[0]
                except IndexError:
                    pass
                else:
                    var_value = self.get_context_varable(var_name)
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

        for root, dirs, files in os.walk(self.get_project_root()):
            for filename in fnmatch.filter(files, '*{{*}}*'):
                try:
                    var_name = get_var_name_pattern.findall(filename)[0]
                except IndexError:
                    pass
                else:
                    var_value = self.get_context_varable(var_name)
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

#    @property
#    def has_pipeline_file(self):
#        """ Detect if the template has a pipeline file. """
#
#        path = os.path.join(self.config._tpl, '.facio.pipeline.yml')
#        if os.path.isfile(path):
#            self.pipeline_file = path
#            self.pipeline = Pipeline(self)
#            return True
#        return False
#
#    def swap_placeholders(self):
#        '''Swap placeholders for real values.'''
#
#        try:
#            from jinja2 import Environment, FileSystemLoader
#        except ImportError:  # pragma: no cover
#            self.config._error('Jinja2 is required for tempalte processing, '
#                               'please install it.')
#
#        cwd = os.getcwd()
#
#        for root, dirs, files in os.walk(self.project_root):
#            jinja_tpl_loader = FileSystemLoader(root)
#            jinja_env = Environment(loader=jinja_tpl_loader)
#            os.chdir(root)
#            ignore_list = self._ignore_list()
#            for f in files:
#                filepath = os.path.join(root, f)
#                exclude = False
#                dirs = filepath.split('/')
#                for d in dirs:
#                    if d in self.exclude_dirs:
#                        exclude = True  # pragma: no cover
#                if not exclude and f not in ignore_list:
#                    try:
#                        tpl = jinja_env.get_template(f)
#                        file_contents = tpl.render(self.place_holders)
#                        with open(filepath, 'w', encoding='utf8') as f:
#                            f.write(file_contents)
#                    except Exception:
#                        import sys
#                        e = sys.exc_info()[1]
#                        with indent(4, quote=' >'):
#                            puts(yellow(
#                                'Warning: Failed to process '
#                                '{0}: {1}'.format(f, e)))
#        os.chdir(cwd)
