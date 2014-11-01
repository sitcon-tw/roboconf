from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from users.models import *
from users.utils import *

@login_required
def edit(request, username):
	user = get_object_or_404(User, username=username)
	privileged = request.user.has_perm('auth.change_user')

	if not (user == request.user or privileged):
		from django.core.exceptions import PermissionDenied
		raise PermissionDenied

	errors = []
	status = ''

	action = request.POST.get('action')
	if action and privileged:
		if action == 'activate':
			user.is_active = True
		elif action == 'deactivate':
			user.is_active = False
		user.save()
		status = 'success'

	if request.POST.get('submit'):
		profile = None
		try:
			profile = user.profile
		except UserProfile.DoesNotExist:
			profile = UserProfile(user=user)

		if privileged:
			username = request.POST.get('username')
			if username != user.username:
				if username:
					if User.objects.filter(username=username).count() < 1:
						user.username = username
					else:
						errors += ['username', 'username_already_taken']
				else:
					errors += ['username', 'invalid_username']

			groups = request.POST.getlist('groups')
			old_groups = user.groups.all()
			for group in old_groups:
				if group.id not in groups:
					user.groups.remove(group)

			for group_id in groups:
				try:
					if group_id not in old_groups:
						user.groups.add(Group.objects.get(id=group_id))
				except Group.DoesNotExist: pass

			profile.title = request.POST.get('title')

		user.first_name = request.POST.get('first_name')
		user.last_name = request.POST.get('last_name')

		email = request.POST.get('email', '')
		if email != user.email:
			try:
				validate_email(email)

				if User.objects.filter(email=email).count() < 1:
					user.email = email
				else:
					errors += ['email', 'email_already_taken']
			except ValidationError:
				errors += ['email', 'invalid_email']

		profile.display_name = request.POST.get('display_name')
		profile.school = request.POST.get('school')
		profile.grade = request.POST.get('grade')
		profile.phone = request.POST.get('phone')
		profile.comment = request.POST.get('comment')

		if len(errors) < 1:
			user.save()
			profile.save()
			status = 'success'
		else:
			status = 'error'

	return render(request, 'users/edit_profile.html', {
		'u': user,
		'categories': sorted_categories if privileged else None,
		'errors': errors,
		'status': status,
	})
