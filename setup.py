#!/usr/bin/env python
"""
Facio
=====

Facio is a project scaffolding tool origionally developed for Django
and expanded to be framework agnostic. You can use facio to bootstrap
any sort of project.
"""

import os
import sys

from setuptools import setup, find_packages

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'src')))

from facio import __version__


install_requires = [
    'GitPython==0.3.2.RC1',
    'Jinja2==2.6',
    'clint2==0.3.2',
    'pycolors2==0.0.2',
]

test_requires = [
    'tox==1.4.2',
    'specloud==0.4.5',
    'coverage==3.5.2',
    'mock==1.0.1',
    'nose==1.1.2',
    'nose-cover3==0.1.0',
    'flake8==1.4',
    'figleaf==0.6.1',
]

dev_requires = test_requires + [
    'ipdb==0.7',
    'ipython==0.13',
    'Sphinx==1.1.3',
]

setup(
    name='facio',
    version=__version__,
    author='Christopher John Reeves',
    author_email='hello@chris.reeves.io',
    url='https://github.com/krak3n/facio',
    description='Project scaffolding using custom templates.',
    long_description=__doc__,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    scripts=['src/facio/bin/facio'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'tests': test_requires,
        'develop': dev_requires,
    },
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='BSD',
)
