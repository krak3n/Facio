# -*- coding: utf-8 -*-

"""
.. module:: facio.vcs
   :synopsis: Classes for cloning remote templates from VCS repositories
"""

import shutil
import tempfile

from facio.base import BaseFacio
from facio.exceptions import FacioException


class BaseVCS(BaseFacio):
    """ Base Version Control System Class all VCS related classes should extend
    from, provides common API. """

    def __init__(self, path):
        """ Simply sets the repository path based.

        :param path: The path to the repository, e.g: git+git@foo.com/bar.git
        :type path: str
        """

        self.vcs, self.path = path.split('+', 1)

    def get_temp_directory(self):
        """ Create a temporary directory to clone the template to.

        :returns: str -- Temp directory path
        """

        try:
            return self.temp_directory_path
        except AttributeError:
            self.temp_directory_path = tempfile.mkdtemp(suffix='facio')
            return self.temp_directory_path

    def clone(self):
        """ This class should be overridden in VCS subclass, if not a
        FacioException will be raised. """

        raise FacioException('The clone method on BaseVCS needs to be '
                             'overridden.')

    def remove_tmp_dir(self, origin, destination):
        """ Template.copy callback function to remove created temp directory.
        """

        shutil.rmtree(origin)


class GitVCS(BaseVCS):
    """ Git Version Control System for cloning git repositories. """

    def clone(self):
        """ Clone the git repository into a temporary directory. """

        try:
            from sh import git
        except ImportError:
            raise FacioException('Git must be installed to use git+ '
                                 'template paths')

        temp_diretory = self.get_temp_directory()

        self.out('Git Cloning {0} to {1}'.format(self.path, temp_diretory))

        try:
            git = git.bake(_cwd=temp_diretory)
            git.clone(self.path, temp_diretory)
            git.fetch('--all')
            git.checkout('master')
        except:
            raise FacioException('Failed to clone git repository '
                                 'at {0}'.format(self.path))

        return temp_diretory


class MercurialVCS(BaseVCS):
    """ Mercurial Version Control System for cloning hg repositories. """

    def clone(self):
        """ Clone the hg repository into a temporary directory. """

        try:
            from sh import hg
        except ImportError:
            raise FacioException('Mercurial must be installed to use hg+ '
                                 'template paths')

        temp_diretory = self.get_temp_directory()

        self.out('Mercurial Cloning {0} to {1}'.format(self.path,
                                                       temp_diretory))

        try:
            hg = hg.bake(_cwd=temp_diretory)
            hg.clone(self.path, temp_diretory)
        except:
            raise FacioException('Failed to clone hg repository '
                                 'at {0}'.format(self.path))

        return temp_diretory
