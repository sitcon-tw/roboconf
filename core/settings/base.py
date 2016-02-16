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

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'core.context_processors.site_url',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
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

AUTHENTICATION_BACKENDS = (
    'users.sitcon_oauth2_authbackend.SITCONOAuth2',
    'django.contrib.auth.backends.ModelBackend',
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
    'social.apps.django_app.default',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'users.oauth_pipeline.save_profile',
    'users.oauth_pipeline.add_to_staffgroup',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
    )

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ISSUE_EXPIRE_TIMEDELTA = datetime.timedelta(hours=12)
ISSUE_DEFAULT_DAYTIME = datetime.time(hour=17)

AVATAR_FILE_SIZE_LIMIT = 2 * (1024 * 1024)
AVATAR_IMAGE_SIZE_LIMIT = 512

BROADCAST_MAGIC_TOKEN = 'All'
URGENT_MAGIC_TOKEN = '#!'

SITCON_OAUTH2_AUTHORIZATION_URL = 'https://staff.sitcon.org/o/authorize'
SITCON_OAUTH2_ACCESS_TOKEN_URL = 'https://staff.sitcon.org/o/token/'
SITCON_OAUTH2_REVOKE_TOKEN_URL = 'https://staff.sitcon.org/o/revoke_token'
SITCON_OAUTH2_USER_DATA_URL = 'https://staff.sitcon.org/api/me'

from .local_settings import *
