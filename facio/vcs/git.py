"""
facio.vcs.git
-------------

Git Version Control Template Cloning.
"""


class Git(object):

    def __init__(self, template_path):
        self.template_path = template_path

    @property
    def repo(self):
        if not hasattr(self, '_repo'):
            self._repo = self.template_path.replace('git+', '')
        return self._repo

    def clone(self):
        pass
