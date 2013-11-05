from django.utils.encoding import force_bytes

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

def generate_nid(node):
    try:
        nid = node.id
    except AttributeError:
        nid = node
    return urlsafe_base64_encode(force_bytes(nid))

def parse_nid(model, nidb64):
	try:
		nid = urlsafe_base64_decode(nidb64)
		return model.objects.get(id=nid)
	except (TypeError, ValueError, OverflowError, model.DoesNotExist):
		return None
