#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from facio import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = [
    'Jinja2==2.6',
    'clint2==0.3.2',
    'sh==1.08',
]

test_requires = [
    'mock==1.0.1',
    'tox==1.4.3',
    'nose==1.3',
    'spec==0.11.1',
    'nose-cov==1.6',
]

dev_requires = test_requires + [
    'ipdb==0.7',
    'ipython==0.13',
    'Sphinx==1.1.3',
    'flake8==2.0',
]

setup(
    name='facio',
    version=__version__,
    author='Christopher John Reeves',
    author_email='hello@chris.reeves.io',
    url='https://github.com/krak3n/facio',
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
