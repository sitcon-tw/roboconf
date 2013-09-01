from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import *
from users.utils import validate_email

@login_required
def profile(request, id):
	u = get_object_or_404(User, pk=id)
	return render(request, 'users_profile.html', {
		'u': u,
	})
