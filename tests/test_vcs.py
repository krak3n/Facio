# -*- coding: utf-8 -*-

"""
.. module:: tests.test_vc
   :synopsis: Tests for the Facio vcs module.
"""

import os

from facio.exceptions import FacioException
from facio.vcs import BaseVCS, GitVCS, MercurialVCS
from mock import patch

from . import BaseTestCase


class TestBaseVCS(BaseTestCase):

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
            'facio.exceptions.puts',
        ])

    def test_repository_path(self):
        instance = BaseVCS('git+/foo/+bar')

        self.assertEqual(instance.path, '/foo/+bar')
        self.assertEqual(instance.vcs, 'git')

    @patch('facio.vcs.tempfile.mkdtemp', return_value='/tmp/foo')
    def test_get_temp_directory(self, mock_tempfile):
        instance = BaseVCS('git+/foo/bar')
        path = instance.get_temp_directory()
        mock_tempfile.return_value = '/tmp/bar'

        mock_tempfile.assert_called_with(suffix='facio')
        self.assertEqual(path, instance.get_temp_directory())

    @patch('sys.exit')
    def test_clone_raises_exception(self, mock_exit):
        instance = BaseVCS('git+/foo/bar')

        with self.assertRaises(FacioException):
            instance.clone()
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: The clone method on BaseVCS needs to be overridden.')

    def test_rm_temp_dir(self):
        instance = BaseVCS('git+/foo/bar')
        d = instance.get_temp_directory()

        instance.remove_tmp_dir(d, '/foo/bar')

        self.assertFalse(os.path.isdir(d))


class TestGitVCS(BaseTestCase):

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
            'facio.exceptions.puts',
        ])

    @patch('sys.exit')
    @patch('sh.Environment.__getitem__', side_effect=ImportError)
    def test_git_not_installed_clone_exception(self, mock_sh, mock_exit):
        instance = GitVCS('git+/foo/bar')

        with self.assertRaises(FacioException):
            instance.clone()
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: Git must be installed to use git+ template paths')

    @patch('sys.exit')
    @patch('sh.git.bake', side_effect=Exception)
    def test_git_clone_fail_exception_raised(self, mock_clone, mock_exit):
        instance = GitVCS('git+/foo/bar')

        with self.assertRaises(FacioException):
            instance.clone()
        self.assertTrue(mock_exit.called)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: Failed to clone git repository at /foo/bar')

    @patch('facio.vcs.tempfile.mkdtemp', return_value='/tmp/foo')
    @patch('sh.git',)
    def test_calls_to_git(self, mock_git, mock_tempfile):
        instance = GitVCS('git+/foo/bar')
        instance.clone()

        mock_git.bake.assert_called_with(_cwd='/tmp/foo')


class TestMercurialVCS(BaseTestCase):

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
            'facio.exceptions.puts',
        ])

    @patch('sys.exit')
    @patch('sh.Environment.__getitem__', side_effect=ImportError)
    def test_git_not_installed_clone_exception(self, mock_sh, mock_exit):
        instance = MercurialVCS('hg+/foo/bar')

        with self.assertRaises(FacioException):
            instance.clone()
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: Mercurial must be installed to use hg+ template paths')

    @patch('sys.exit')
    @patch('sh.hg.bake', side_effect=Exception)
    def test_hg_clone_fail_exception_raised(self, mock_clone, mock_exit):
        instance = MercurialVCS('hg+/foo/bar')

        with self.assertRaises(FacioException):
            instance.clone()
        self.assertTrue(mock_exit.called)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: Failed to clone hg repository at /foo/bar')

    @patch('facio.vcs.tempfile.mkdtemp', return_value='/tmp/foo')
    @patch('sh.hg',)
    def test_calls_to_hg(self, mock_hg, mock_tempfile):
        instance = MercurialVCS('hg+/foo/bar')
        instance.clone()

        mock_hg.bake.assert_called_with(_cwd='/tmp/foo')
