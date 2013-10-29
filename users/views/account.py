from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.debug import sensitive_post_parameters, sensitive_variables
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from users.forms import PasswordResetForm
from users.token import parse_token, check_token

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

def reset_password(request, user=None):
	form = PasswordResetForm()
	success = None

	if request.method == 'POST':
		form = PasswordResetForm(request.POST)
	elif request.user.has_perm('auth.change_user'):		# Prefill user email
		try:
			user = User.objects.get(id=request.GET.get('id'))
			form = PasswordResetForm({'email': user.email})
		except User.DoesNotExist:
			pass

	if form.is_valid():
		form.save()
		success = True

	return render(request, 'users_reset_password.html', {'form': form, 'success': success})

@sensitive_variables
@sensitive_post_parameters
def reset_password_confirm(request, token):
	user, token_state = parse_token(token)
	if user is not None and check_token(user, token_state):
		if request.method == 'POST':
			form = SetPasswordForm(user, request.POST)
			if form.is_valid():
				form.save()
				return redirect(reverse('users:login') + '?status=reset_successful')
		else:
			form = SetPasswordForm(user)
	else:
		form = None

	return render(request, 'users_set_password.html', {'form': form})
