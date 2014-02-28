# -*- coding: utf-8 -*-
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'roboconf', 
        'USER': 'postgres', 
        'PASSWORD': '',
        'HOST': '127.0.0.1', 
        'PORT': '',
    }
}

