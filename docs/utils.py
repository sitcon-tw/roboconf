from django.core.exceptions import ObjectDoesNotExist
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
        nid = node.id + getattr(node.model._meta, 'nid_namespace', '')
    except AttributeError:
        nid = node
    return urlsafe_base64_encode(force_bytes(nid))

def parse_nid(nidb64, model=None):
    try:
        nid = urlsafe_base64_decode(nidb64)
        if nid[-1:] == 'F':
            from docs.models import File
            return File.objects.get(id=nid[:-1])
        elif nid[-1:] == 'D':
            from docs.models import Folder
            return Folder.objects.get(id=nid[:-1])
        else:
            if not model: return None
            return model.objects.get(id=nid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
          return None
