from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_bytes
from docs.models import File, Folder

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

NID_NAMESPACES = {'F': File, 'D': Folder}

def generate_nid(text):
    return urlsafe_base64_encode(force_bytes(text))

def parse_nid(nidb64):
    try:
        nid = urlsafe_base64_decode(nidb64)
        model = NID_NAMESPACES[nid[-1:]]
        return model.objects.get(id=nid[:-1])
    except (TypeError, ValueError, OverflowError, KeyError, ObjectDoesNotExist):
        return None

def get_uid(model, id):
    return generate_nid(force_bytes(id) + model.Meta.nid_namespace)
