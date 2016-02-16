from django.contrib.auth.models import User, Group
from django.utils.timezone import now
from django.db.transaction import rollback
from django.db import connection
from docs.models import *
from docs.perms import *
from docs.utils import *

# NOTE: For Django shell debugging use only
# DO NOT INCLUDE IN PRODUCTION USE

def all(model):
    return model.objects.all()

def user(id=1):        # Admin account
    return User.objects.get(id=id)

def folder(id=1):    # Root folder
    return Folder.objects.get(id=id)

def file(id):
    return File.objects.get(id=id)

def permobj(id):
    return Permission.objects.get(id=id)

def rev(id):
    return Revision.objects.get(id=id)

def btext(id):
    return BlobText.objects.get(id=id)

def sql(statement):
    cursor = connection.cursor()
    cursor.execute(statement)
