# -*- coding: utf-8 -*-
import os
import dj_database_url
from .base import *

DATABASES = {
	'default': dj_database_url.config()
}

DEBUG = False
TEMPLATE_DEBUG = False

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['staff.sitcon.org']

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = u'"SITCON 行政系統" <admin@staff.sitcon.org>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

DEFAULT_NOTIFICATION_SENDER = u'SITCON 行政系統:notifications@staff.sitcon.org'
DEFAULT_ACCOUNTS_SENDER =  u'SITCON 行政系統:accounts@staff.sitcon.org'
DEFAULT_ISSUE_SENDER = u'SITCON 行政系統:issues@staff.sitcon.org'

SUBMITTER_ACCOUNTS_SENDER = u'SITCON:accounts@staff.sitcon.org'
USER_ISSUE_SENDER = '{0} (SITCON):issues@staff.sitcon.org'

SMS_API_KEY = os.environ.get('SMS_API_KEY')
SMS_API_SECRET = os.environ.get('SMS_API_SECRET')
DEFAULT_SMS_SENDER = 'SITCON'
