#!/usr/bin/env python
"""
{{ PROJECT_NAME }}
------------------
"""

from setuptools import setup, find_packages
from {{ PROJECT_NAME }} import __version__


setup(
    name="{{ PROJECT_NAME }}",
    version=__version__,
    author='{{ AUTHOR }}',
    author_email='{{ AUTHOR_EMAIL }}',
    packages=find_packages(
        exclude=['examples', 'tests']),
)
