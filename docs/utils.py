from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from docs.models import File, Folder

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

def get_nid(model, id):
    return generate_nid(force_bytes(id) + model.nid_namespace)
