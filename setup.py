#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages
from skeletor import VERSION

setup(
    name="Skeletor",
    version=VERSION,
    url='https://github.com/krak3n/Skeletor',
    author='Christopher Reeves',
    author_email='hello@chris.reeves.io',
    description='A django project skeleton generator similar to django '
                'startproject',
    packages=find_packages(exclude=['examples', 'tests']),
    install_requires=['GitPython==0.3.2.RC1', 'Jinja2==2.6'],
    scripts=['skeletor/bin/skeletor'],
)
