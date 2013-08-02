from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from users.models import *

def profile(request, id):
	u = get_object_or_404(User, pk=id)
	return render(request, 'users_profile.html', {
		'u': u,
	})

def edit_profile(request, id):
	u = get_object_or_404(User, pk=id)
	
	if not (u == request.user or request.user.has_perm('auth.change_user')):
		return redirect(reverse('users:list'))

	return render(request, 'users_change_profile.html', {
		'u': u,
	})
