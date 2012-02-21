#!/usr/bin/env python
# encoding: utf-8

import os
from setuptools import setup
from skeletor import VERSION

setup(
    name="Skeletor",
    version=VERSION,
    url='https://github.com/krak3n/Skeletor',
    author='Christopher Reeves',
    author_email='me@chris-reeves.com',
    description='A django project skeleton generator similar to django '\
                'startproject',
    packages=['skeletor',],
    install_requires=['GitPython==0.3.2.RC1',],
    scripts=['skeletor/bin/skeletor'],
)
