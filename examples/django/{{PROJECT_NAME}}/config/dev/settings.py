"""
{{ PROJECT_NAME }}.config.settings.dev
--------------------------------------
"""

from ..common.settings import *


""" Debugging (default True for local environment) """
DEBUG = True
TEMPLATE_DEBUG = DEBUG

""" Databases (default is mysql) """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ PROJECT_NAME }}',
        'USER': 'root',
        'PASSWORD': '',
    }
}

""" Cacheing (default is dummy, see django docs) """
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

""" Use MD5 Password Hashing for Dev - Speeds things up """
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
