from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.models import User
from django import forms
import re

from notifications.utils import format_address, send_template_mail
from users.models import RegisterToken
from users.token import generate_uid, generate_token
from users.models import UserProfile



class PasswordResetForm(DjangoPasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email__iexact=email)
            if not user.has_usable_password():
                raise ValidationError("Reset unavailable", code='reset_unavailable')
        except User.DoesNotExist:
            raise ValidationError("Invalid email", code='invalid_email')
        return email

    def save(self):
        email = self.cleaned_data['email']
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        for user in active_users:
            if not user.has_usable_password():
                continue

            context = {
                'receiver': user,
                'uid': generate_uid(user),
                'token': generate_token(user),
            }

            sender_address = settings.DEFAULT_ACCOUNTS_SENDER
            receiver_address = format_address(user.profile.name, user.email)
            send_template_mail(sender_address, receiver_address, 'mail/user_reset_password.html', context)


class RegisterForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', )

    def clean_username(self):
        username = self.cleaned_data.get('username', False)
        if not (User.objects.filter(username=username).count() < 1 and username):
            raise ValidationError("Username taken", code='username_taken')
        elif not re.match(r'[0-9A-Za-z_@\+\.\-]+', username):
            raise ValidationError("Invalid username", code="invalid_username")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', False)
        validate_email(email)
        if not (User.objects.filter(email=email).count() < 1 and email):
            raise ValidationError("Email used", code='email_used')
        return email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class TokenEditForm(forms.models.ModelForm):
    class Meta:
        model = RegisterToken
        fields = ('username', 'email', 'title', 'display_name', 'groups', 'valid')
