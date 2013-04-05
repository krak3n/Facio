#
# Sphinx Documentation Config
#

import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath('.'), '..', 'src',
                                'facio'))

project = u'Facio'
copyright = u'2013, Christopher Reeves'

version = '1.1'
release = '1.1.0'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['_static']

latex_elements = {
}

latex_documents = [
    ('index', 'Facio.tex', u'Facio Documentation',
     u'Christopher Reeves', 'manual'),
]

man_pages = [
    ('index', 'facio', u'Facio Documentation',
     [u'Christopher Reeves'], 1)
]

texinfo_documents = [
    ('index', 'Facio', u'Facio Documentation',
     u'Christopher Reeves', 'Facio', 'Project scaffolding from custom '
     'templates.', 'Miscellaneous'),
]
