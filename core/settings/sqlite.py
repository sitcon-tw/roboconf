# -*- coding: utf-8 -*-
from .base import *
from .vendor import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'roboconf.db'),
    }
}
