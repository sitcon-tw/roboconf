# -*- coding: utf-8 -*-
import os
import json

SETTINGS_DIR = os.path.dirname(__file__)

if os.path.exists(os.path.join(SETTINGS_DIR, '/settings.json')):
    with open(os.path.join(SETTINGS_DIR, '/settings.json'), 'r') as f:
        os.environ.update(json.load(f))

if 'HEROKU' in os.environ:
    from .heroku import *
elif 'DEBUG' in os.environ:
    from .sqlite import *
else:
    from .postgres import *
