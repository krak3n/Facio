# -*- coding: utf-8 -*-

"""
.. module:: facio.vcs
   :synopsis: Classes for cloning remote templates from VCS repositories
"""

import tempfile

from facio import Facio
from facio.exceptions import FacioException


class BaseVCS(Facio):
    """ Base Version Control System Class all VCS related classes should extend
    from, provides common API. """

    def __init__(self, path):
        """ Simply sets the repository path based.

        :param path: The path to the repository, e.g: git+git@foo.com/bar.git
        :type path: str
        """

        vcs, path = path.split('+', 1)
        self.path = path

    def get_temp_directory(self):
        """ Create a temporary directory to clone the template too.

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


class GitVCS(BaseVCS):
    """ Git Version Control System for cloning git repositories. """

    def clone(self):
        """ Clone the git repository into a temporary directory. """

        try:
            from sh import git
        except ImportError:
            raise FacioException('Git must be installed to use git+ '
                                 'template paths.')

        temp_diretory = self.get_temp_directory()

        try:
            git = git.bake(_cwd=temp_diretory)
            git.clone(self.path, temp_diretory)
            git.fetch('--all')
            git.checkout('master')
        except:
            import sys
            e = sys.exc_info()[1]
            raise FacioException('Failed to clone git repository: '
                                 '{0}'.format(e))


class MercurialVCS(BaseVCS):
    """ Mercurial Version Control System for cloning hg repositories. """

    def clone(self):
        """ Clone the hg repository into a temporary directory. """

        try:
            from sh import hg
        except ImportError:
            raise FacioException('Git must be installed to use git+ '
                                 'template paths.')

        temp_diretory = self.get_temp_directory()

        try:
            hg = hg.bake(_cwd=temp_diretory)
            hg.clone(self.path, temp_diretory)
        except:
            import sys
            e = sys.exc_info()[1]
            raise FacioException('Failed to clone hg repository: '
                                 '{0}'.format(e))
