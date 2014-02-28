# -*- coding: utf-8 -*-
import os

if "HEROKU" in os.environ:
	from .heroku import *
else:
	from .sqlite import *
