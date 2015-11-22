# -*- coding: utf-8 -*-
# DEVELOPERS: Django or server related settings which are mostly the same across sites should be kept here
from __future__ import unicode_literals
import os
import datetime
from django.conf import global_settings

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[0:-2])

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

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

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'core.context_processors.site_url',
)

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
    'submission',
    'schedule',
    'rest_framework',
    'api',
    'imagekit',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['file'],
            'propagate': False,
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'file': {
            'level': 'DEBUG',
            'filename': 'roboconf.log',
            'formatter': 'verbose',
            'class': 'logging.FileHandler'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(module)s %(process)d %(thread)d %(message)s'
        }
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ISSUE_EXPIRE_TIMEDELTA = datetime.timedelta(hours=12)
ISSUE_DEFAULT_DAYTIME = datetime.time(hour=17)

AVATAR_FILE_SIZE_LIMIT = 2 * (1024 * 1024)
AVATAR_IMAGE_SIZE_LIMIT = 512

BROADCAST_MAGIC_TOKEN = 'All'
URGENT_MAGIC_TOKEN = '#!'

from .local_settings import *
