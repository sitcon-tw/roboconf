# -*- coding: utf-8 -*-
import os

if 'HEROKU' in os.environ:
	from .heroku import *
elif 'DEBUG' in os.environ:
	from .sqlite import *
else:
	from .postgres import *
