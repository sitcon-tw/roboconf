# -*- coding: utf-8 -*-
import os
import json

SETTINGS_DIR = os.path.dirname(__file__)

if 'HEROKU' in os.environ:
    from .heroku import *
elif 'DEBUG' in os.environ:
    from .sqlite import *
else:
    from .postgres import *
