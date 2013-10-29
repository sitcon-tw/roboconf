from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from notifications.utils import get_mail_setting, format_address, send_template_mail
from users.utils import get_user_name
from users.token import generate_token

class PasswordResetForm(DjangoPasswordResetForm):
	def clean_email(self):
		data = self.cleaned_data['email']
		try:
			user = User.objects.get(email__iexact=email)
			if not user.has_usable_password():
				raise forms.ValidationError("Reset unavailable", code='reset_unavailable')
		except User.DoesNotExist:
			raise forms.ValidationError("Invalid email", code='invalid_email')
		return data

	def save(self):
		email = self.cleaned_data['email']
		active_users = User.objects.filter(email__iexact=email, is_active=True)
		for user in active_users:
			if not user.has_usable_password():
				continue

			context = {
				'receiver': user,
				'token': generate_token(user),
			}

			sender_address = get_mail_setting('sender', 'account')
			receiver_address = format_address(get_user_name(user), user.email)
			send_template_mail(sender_address, receiver_address, 'mail/user_reset_password.html', context)
