# -*- coding: utf-8 -*-
# DEVELOPERS: Django or server related settings which are mostly the same across sites should be kept here

import os
import datetime
from django.conf import global_settings

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[0:-2])

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

LOGIN_URL = 'users:login'

TIME_ZONE = 'Asia/Taipei'
LANGUAGE_CODE = 'zh-tw'

SITE_ID = 1
USE_I18N = True    # TODO: Implement internationalization
USE_L10N = True
USE_TZ = True

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + [
    'core.context_processors.site_url',
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = ()

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'core',
    'users',
    'docs',
    'issues',
    'agenda',
    'notifications',
    'rest_framework',
    'api',
    'oauth2_provider',
    'imagekit',
    'corsheaders',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        ],
    'DEFAULT_PERMISSION_CLASSES': [],
}

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read_personal_data': 'Read username, first_name, last_name, email, groups and other public fields',
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ISSUE_EXPIRE_TIMEDELTA = datetime.timedelta(hours=12)
ISSUE_DEFAULT_DAYTIME = datetime.time(hour=17)

AVATAR_FILE_SIZE_LIMIT = 2 * (1024 * 1024)
AVATAR_IMAGE_SIZE_LIMIT = 512

BROADCAST_MAGIC_TOKEN = 'All'
URGENT_MAGIC_TOKEN = '#!'

from .local_settings import *
