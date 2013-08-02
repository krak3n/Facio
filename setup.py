#!/usr/bin/env python

import os
import sys
import multiprocessing  # NOQA

from setuptools import setup, find_packages

major, minor, micro, release, serial = sys.version_info

IS_PY26 = False
if major == 2 and minor == 6:
    IS_PY26 = True

INSTALL_YAML = False
try:
    import yaml  # NOQA
except ImportError:
    INSTALL_YAML = True

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import facio
version = facio.get_version()


def read(fname):
    return open(fname).read()


install_requires = [
    'Jinja2==2.6',  # For python >= 3.2
    'clint2==0.3.2',
    'sh==1.08',
    'six==1.3.0',
    'docopt==0.6.1'
]
if IS_PY26:
    install_requires = install_requires + [
        'importlib',
    ]
if INSTALL_YAML:
    install_requires = install_requires + [
        'PyYAML',
    ]

test_requires = [
    'mock==1.0.1',
    'tox==1.4.3',
    'nose==1.3',
    'coverage==3.6',
    'coveralls == 0.2',
]
if IS_PY26:
    test_requires = test_requires + [
        'unittest2',
    ]

dev_requires = test_requires + [
    'pdbpp==0.7',
    'ipython==0.13.2',
    'Sphinx==1.1.3',
    'flake8==2.0',
]

setup(
    name='facio',
    version=version,
    author='Christopher John Reeves',
    author_email='hello@chris.reeves.io',
    url='http://facio.readthedocs.org',
    description='Project scaffolding using custom templates.',
    long_description=read('README.rst'),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    scripts=['src/facio/bin/facio'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    test_suite='runtests.runtests',
    extras_require={
        'test': test_requires,
        'develop': dev_requires,
    },
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='BSD'
)
