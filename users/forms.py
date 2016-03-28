from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.models import User
from django import forms

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
                'reset_link': reverse('users:reset_password_confirm', args=(generate_uid(user), generate_token(user))),
            }

            sender_address = settings.DEFAULT_ACCOUNTS_SENDER
            receiver_address = format_address(user.profile.name, user.email)
            send_template_mail(sender_address, receiver_address, 'mail/user_reset_password.html', context)


class RegisterForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class TokenEditForm(forms.models.ModelForm):
    class Meta:
        model = RegisterToken
        fields = ('username', 'email', 'title', 'groups', 'valid')
