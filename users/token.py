from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

# == snippet from Django 1.6 dev snapshot ==
# ** remove when 1.6 offically came out **
import base64

def urlsafe_base64_encode(s):
    """
    Encodes a bytestring in base64 for use in URLs, stripping any trailing
    equal signs.
    """
    return base64.urlsafe_b64encode(s).rstrip(b'\n=')

def urlsafe_base64_decode(s):
    """
    Decodes a base64 encoded string, adding back any trailing equal signs that
    might have been stripped.
    """
    s = s.encode('utf-8') # base64encode should only return ASCII.
    try:
        return base64.urlsafe_b64decode(s.ljust(len(s) + len(s) % 4, b'='))
    except (LookupError, BinasciiError) as e:
        raise ValueError(e)
# == end snippet ==

def generate_token(user):
	uid = urlsafe_base64_encode(force_bytes(user.pk))
	token = default_token_generator.make_token(user)
	return '_'.join((uid, token))

def parse_token(token):
	try:
		token_uid, token_state = str(token).split('-')
		uid = urlsafe_base64_decode(token_uid)
		return (User.objects.get(pk=uid), token_state)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		return (None, None)

def check_token(user, token):
	return default_token_generator.check_token(user, token)
