"""
{{ PROJECT_NAME }}.config.common.settings
-----------------------------------------
"""

from os.path import abspath, join, dirname


""" Paths """
SITE_ROOT = abspath(join(dirname(__file__), '..', '..'))
PROJECT_ROOT = abspath(join(dirname(__file__), '..', '..'))
MEDIA_ROOT = join(SITE_ROOT, 'media')
STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'public'), ]
LOG_ROOT = join(SITE_ROOT, 'logs')

""" Urls """
STATIC_URL = '/s/'
MEDIA_URL = '/m/'
ROOT_URLCONF = '{{ PROJECT_NAME }}.urls'

""" Secret Key & Site ID """
SITE_ID = 1
SECRET_KEY = '{{ DJANGO_SECRET_KEY }}'

""" Location """
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
USE_I18N = True
USE_L10N = True

""" Templates """
TEMPLATE_DIRS = [join(PROJECT_ROOT, 'templates')]
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    '{{ PROJECT_NAME }}.context_processors.domain',
)

""" Middleware """
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

""" Installed Applications """
INSTALLED_APPS = (
    # Django Apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    # Third Party Apps here
    # Project Apps here
)

""" Test Suite """
NOSE_ARGS = [
    '--include=^(can|it|ensure|must|should|specs?|examples?)',
    '--with-spec',
    '--spec-color',
    '-s',
    '--with-coverage',
    '--cover-erase',
    '--cover-package={{ PROJECT_NAME }}']
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
