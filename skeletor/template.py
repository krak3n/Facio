#!/usr/bin/env python
# encoding: utf-8


import os
import re
import sys
import tempfile
try:
    from git import Repo
except ImportError:
    print 'GitPython module missing, please install it.'
    sys.exit()
from shutil import copytree, move, rmtree, copy


class Template(object):

    is_git = False
    complete = False
    place_holders = {
        'PROJECT_NAME': 'project_name',
        'SETTINGS_DIR': 'template_settings_dir',
        'DB_NAME': 'db_name',
        'DB_USER': 'db_user',
        'DB_PASS': 'db_pass',
        'DJANGO_SECRET_KEY': 'django_secret_key'}

    def __init__(self, config):

        self.config = config
        self.working_dir = os.popen('pwd').read().split()[0]
        self.set_project_root()
        self.is_git()
        self.copy_template()

    def set_project_root(self):
        '''Set project root, based on working dir and project name.'''

        self.project_root = os.path.join(self.working_dir,
                                         self.config.project_name)

    def make_project_dir(self):
        '''Make the project director in current working directory.'''

        if not os.path.isdir(self.project_root):
            os.mkdir(self.project_root)
            if not os.path.isdir(self.project_root):
                self.config.cli_opts.error('Error creating project '
                                           'directory')
        else:
            self.config.cli_opts.error('%s already exists' % (
                self.project_root))

# TODO: git stuff should live in its own class
    def is_git(self):
        '''Detect if the user wants to use a git repository.'''

        if self.config.template.startswith('git+'):
            self.is_git = True
            self.git_repo_path = self.config.template.replace('git+', '')
            self.config.template = tempfile.mkdtemp(suffix='skeletor')
            print 'Using git to clone template from %s' % self.git_repo_path
            self.git_clone()

    def git_clone(self):
        '''Clone git repository into tmp directory.'''

        try:
            repo = Repo.init(self.config.template)
            repo.create_remote('origin', self.git_repo_path)
            origin = repo.remotes.origin
            origin.fetch()
            origin.pull('master')
        except:
            self.config.cli_opts.error('Error cloning repository')
        else:
            rmtree(os.path.join(self.config.template, '.git'))

    def copy_template(self):
        '''Moves template into current working dir.'''

        if os.path.isdir(self.config.template):
            self.make_project_dir()
            for file in os.listdir(self.config.template):
                path = os.path.join(self.config.template, file)
                if os.path.isdir(path):
                    copytree(path, os.path.join(self.project_root, file))
                else:
                    copy(path, self.project_root)
            self.swap_placeholders()
        else:
            self.config.cli_opts.error('Unable to copy template, directory '
                                       'does not exist')
        if self.is_git:
            rmtree(self.config.template)

    def rename(self, root, name):
        '''Rename a file or directory.'''

        e = re.compile(r'{{(.*?)}}')
        try:
            plain = e.findall(name)[0]
            if plain in self.place_holders:
                place_holder_val = getattr(self.config,
                                           self.place_holders[plain])
                origin = os.path.join(root, name)
                new_name = name.replace('{{%s}}' % plain, place_holder_val)
                new = os.path.join(root, new_name)
                move(origin, new)
        except IndexError:
            pass

    def rename_directories(self):
        '''Move directories with placeholder names.'''

        for root, dirs, files in os.walk(self.project_root):
            for d in dirs:
                self.rename(root, d)
        return False

    def rename_files(self):
        '''Move files with placeholder names.'''

        for root, dirs, files in os.walk(self.project_root):
            for f in files:
                self.rename(root, f)
        return False

    def replace_line(self, f, line, placeholder):
        '''Replace placeholder with value.'''

        attr = self.place_holders[placeholder]
        val = getattr(self.config, attr, None)
        if val:
            line = line.replace('{{%s}}' % placeholder, val)
            f.write(line)

    def swap_placeholders(self):
        '''Swap placeholders for real values.'''

        while self.rename_directories():
            continue

        while self.rename_files():
            continue

        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                filepath = os.path.join(root, file)
                with open(filepath, 'r+') as f:
                    lines = f.readlines()
                    f.seek(0)
                    f.truncate()
                    for line in lines:
                        has_placeholder = False
                        for placeholder in self.place_holders:
                            if '{{%s}}' % placeholder in line:
                                has_placeholder = True
                                self.replace_line(f, line, placeholder)
                        if not has_placeholder:
                            f.write(line)
                    f.close()
