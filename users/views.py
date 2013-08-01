from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters, sensitive_variables
import django.contrib.auth as auth

import views_list as _list
import views_profile as _profile

@sensitive_post_parameters('password')
def login(request):
	if request.user.is_authenticated():
		return redirect(reverse('index'))

	context = {}
	if 'submit' in request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth.login(request, user)
				
				# Do redirection if provided
				url = request.POST.get('next')
				url = reverse('index') if (not url) or ('//' in url) else url
				return redirect(url)
			context['error'] = 'account_disabled'
		else:
			context['error'] = 'invalid_login'

	url = request.REQUEST.get('next')
	context['redirect_url'] = url
	return render(request, 'users_login.html', context)

def logout(request):
	auth.logout(request)
	return redirect(reverse('users:login'))

@login_required
def list(request):
	return _list.list(request)

@login_required
def profile(request, id):
	return _profile.profile(request, id)

@login_required
@sensitive_variables()
@sensitive_post_parameters()
def change_password(request):
	status = ''
	old_password = request.POST.get('old_password')
	new_password = request.POST.get('new_password')
	verify_password = request.POST.get('verify_password')
	if old_password and new_password and verify_password:
		if request.user.check_password(old_password):
			if new_password == verify_password:
				request.user.set_password(new_password)
				request.user.save()
				status = 'success'
			else: status = 'password_mismatch'
		else: status = 'invalid_login'
	return render(request, 'users_change_password.html', {'status': status})
