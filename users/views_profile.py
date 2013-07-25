from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import *

def profile(request, id):
	return render(request, 'users_profile.html', {})
