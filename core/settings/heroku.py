# -*- coding: utf-8 -*-
import os
import dj_database_url
from .base import *
from .vendor import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

SMS_API_KEY = os.environ.get('SMS_API_KEY')
SMS_API_SECRET = os.environ.get('SMS_API_SECRET')
