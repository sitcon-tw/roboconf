from django.shortcuts import render
from django.views.decorators.debug import sensitive_variables
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group
from users.models import *
from users.utils import *
from notifications.utils import send_template_mail, format_address

@sensitive_variables('password')
@permission_required('auth.add_user', login_url='users:list')
def create(request):
	errors = []
	status = ''

	if 'submit' in request.POST:
		user = User()

		username = request.POST.get('username')
		if username:
			if User.objects.filter(username=username).count() < 1:
				user.username = username
			else:
				errors += ['username', 'username_already_taken']
		else:
			errors += ['username', 'invalid_username']

		email = request.POST.get('email', '')
		if validate_email(email):
			if User.objects.filter(email=email).count() < 1:
				user.email = email
			else:
				errors += ['email', 'email_already_taken']
		else:
			errors += ['email', 'invalid_email']

		user.first_name = request.POST.get('first_name')
		user.last_name = request.POST.get('last_name')

		password = generate_password()
		user.set_password(password)

		if len(errors) < 1:
			user.save()		# Save the user first in order to create relational objects

			profile = UserProfile(user=user)
			profile.title = request.POST.get('title')
			profile.display_name = request.POST.get('display_name')
			profile.school = request.POST.get('school')
			profile.grade = request.POST.get('grade')
			profile.phone = request.POST.get('phone')
			profile.comment = request.POST.get('comment')
			profile.save()

			for group_id in request.POST.getlist('groups'):
				try:
					user.groups.add(Group.objects.get(id=group_id))
				except Group.DoesNotExist: pass

			user.save()		# Save the groups information

			if request.POST.get('send_welcome_letter'):
				context = {
					'sender': request.user,
					'receiver': user,
					'password': password,
					'groups': [g.name for g in user.groups.all()],
				}

				sender_address = format_address(get_user_name(request.user), request.user.email)
				receiver_address = format_address(get_user_name(user), user.email)
				send_template_mail(sender_address, receiver_address, 'mail/user_welcome.html', context)

			status = 'success'
		else:
			status = 'error'

	return render(request, 'users/create.html', {
		'categories': GroupCategory.objects.all(),
		'errors': errors,
		'status': status,
	})
