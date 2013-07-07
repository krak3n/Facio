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
from sh import pwd

from facio.base import BaseFacio
from facio.exceptions import FacioException
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
        self.update_context_variables({
            'PROJECT_NAME': name
        })

        # Update ignore globs with standard ignore patterns
        self.update_ignore_globs([
            '.git',
            '.hg',
            '.svn',
            '*.pyc',
        ])

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

    def update_context_variables(self, dictionary):
        """ Update the context varaibles dict with new values.

        ** Usage: **

        .. code-block:: python

            from facio.template import Template
            dictionary = {
                'bar': 'baz',
                'fib': 'fab',
            }
            t = Template('foo', '/path/to/foo')
            t.update_context_variables(dictionary)

        :param dictionary: Dictionary of new key values
        :type dictionary: dict
        """

        try:
            dict1 = self.context_variables
        except AttributeError:
            self.context_variables = {}
            dict1 = self.context_variables
        dict2 = dictionary

        if isinstance(dict1, dict) and isinstance(dict2, dict):
            dict1.update(dict2)
            self.context_variables = dict1
        else:
            raise FacioException('Variable update failed')

    def get_context_variables(self):
        """ Returns the current context variables at time of call.

        :retutns: list
        """

        try:
            return self.context_variables
        except AttributeError:
            return {}

    def get_context_variable(self, name):
        """ Return a specific context variable value.

        :param name: Context variable name
        :type name: str

        :returns: str or None -- None if name not found in var list
        """

        variables = self.get_context_variables()
        return variables.get(name, None)

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
            else:
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

    def get_ignore_files(self, files):
        """ Returns a list of files to ignore based on ``get_ignore_globs``
        patterns.

        :param files: List of files to check against
        :type files: list

        :returns: list -- list of filenames
        """

        ignores = []
        for pattern in self.get_ignore_globs():
            for filename in fnmatch.filter(files, pattern):
                ignores.append(filename)

        return ignores

    def copy(self, callback=None):
        """ Copy template from origin path to ``self.get_project_root()``.

        :param callback: A callback function to be called after copy is comlete
        :type callback: function -- default None

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
                    ('git+', GitVCS),
                    ('hg+', MercurialVCS),
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
                    self.get_project_root()))

        # Call callback if callable
        if callable(callback):
            callback(
                origin=self.path,
                destination=self.get_project_root())

        return True

    def rename_direcories(self):
        """ Renames directories that are named after context variables, for
        example: ``{{PROJECT_NAME}}``.

        :returns: generator
        """

        for root, dirs, files in os.walk(self.get_project_root()):
            for directory in fnmatch.filter(dirs, '*{{*}}*'):
                var_name = get_var_name_pattern.findall(directory)[0]
                var_value = self.get_context_variable(var_name)
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
                var_name = get_var_name_pattern.findall(filename)[0]
                var_value = self.get_context_variable(var_name)
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

    def write(self):
        """ Reads the template and uses Jinja 2 to replace context variables
        with their real values.
        """

        variables = self.get_context_variables()
        for root, dirs, files in os.walk(self.get_project_root()):
            jinja_loader = FileSystemLoader(root)
            jinja_environment = Environment(loader=jinja_loader)
            ignores = self.get_ignore_files(files)
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
