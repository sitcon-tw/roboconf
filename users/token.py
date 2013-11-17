from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

def generate_uid(user):
    return urlsafe_base64_encode(force_bytes(user.pk))

def parse_uid(uidb64):
	try:
		uid = urlsafe_base64_decode(uidb64)
		return User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		return None

def generate_token(user):
    return default_token_generator.make_token(user)
    
def check_token(user, token):
	return default_token_generator.check_token(user, token)
