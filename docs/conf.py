#
# Sphinx Documentation Config
#

import os
import sphinx_bootstrap_theme
import sys

from datetime import datetime

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import facio

now = datetime.now()

project = u'Facio'
copyright = u'{0}, Christopher Reeves'.format(now.year)

version = '{0}.{1}'.format(*facio.__VERSION__[:2])
release = facio.get_version()

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

# Theme
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_static_path = ['_static']

man_pages = [
    ('index', 'facio', u'Facio Documentation',
     [u'Christopher Reeves'], 1)
]

texinfo_documents = [
    ('index', 'Facio', u'Facio Documentation',
     u'Christopher Reeves', 'Facio', 'Project scaffolding from custom '
     'templates.', 'Miscellaneous'),
]
