from django import forms
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from notifications.utils import get_mail_setting, format_address, send_template_email
from users.utils import get_user_name

class PasswordResetForm(DjangoPasswordResetForm):
	def clean_email(self):
		data = self.cleaned_data['email']
		try:
			user = User.objects.get(email__iexact=email)
			if not user.has_usable_password():
				raise forms.ValidationError(code='reset_unavailable')
		except User.DoesNotExist:
			raise forms.ValidationError(code='invalid_email')
		return data

	def save(self):
        email = self.cleaned_data["email"]
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        for user in active_users:
            if not user.has_usable_password():
                continue

            context = {
                'receiver': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }

			sender_address = get_mail_setting('sender', 'account')
			receiver_address = format_address(get_user_name(user), user.email)
			send_template_email(sender_address, receiver_address, 'mail/user_reset_password.html', context)
