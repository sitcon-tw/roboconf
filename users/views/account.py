from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters, sensitive_variables
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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
	status = ''

	# Need permission to reset other users' password by this method
	if request.user.has_perm('auth.change_user'):
		id = request.GET.get('id')
		if id:
			try:
				user = User.objects.get(id=id)
				# Here we don't do validity check since this functionality is restricted to staff
			except User.DoesNotExist:
				pass
	else:
		user = None

	# Try reverse query the user from database
	email = request.POST.get('email')
	if email:
		try:
			user = User.objects.get(email__iexact=email)
			if not user.has_usable_password():
				status = 'reset_unavailable'
				user = None
		except User.DoesNotExist:
			status = 'invalid_email'

	if user:
		# Generate reset token
		token = token_generator.make_token(user)
		context = {
			'receiver': user,
			'token': token,
		}

		sender_address = get_mail_setting('sender', 'account')
		receiver_address = format_address(get_user_name(user), user.email)
		send_template_email(sender_address, receiver_address, 'mail/user_reset_password.html', context)
		status = 'success'

	return render(request, 'users_reset_password.html', {'status': status})

@sensitive_variables
@sensitive_post_parameters
def reset_password_confirm(request, token):
	status = ''

	return render(request, 'users_change_password.html', {'status': status})
