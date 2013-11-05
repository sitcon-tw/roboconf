from django.contrib.auth.models import User, Group
from django.db import connection
from docs.models import *
from docs.perms import *
from docs.utils import *

# NOTE: For Django shell debugging use only
# DO NOT INCLUDE IN PRODUCTION USE

def user(id=1):		# Admin account
	return User.objects.get(id=id)

def folder(id=0):	# Root folder
	return Folder.objects.get(id=id)

def sql(statement):
	cursor = connection.cursor()
	cursor.execute(self)
