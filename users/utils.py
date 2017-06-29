from users.models import *
from core.settings import *
import re

def generate_password():
    from os import urandom
    from base64 import urlsafe_b64encode
    # Generate a password with length 12
    return urlsafe_b64encode(urandom(8))[:-1]

def get_user_sorting_key(user):
    groups = [g.id for g in user.groups.all()]
    identity = ''.join([str(1 - groups.count(i)) for i in GROUP_PRIORITY])    # Sort by identity first
    name = user.profile.name
    return ''.join((identity, name))

def sorted_users(users):
    return sorted(users, key=get_user_sorting_key)

def sorted_tokens(tokens):
    return sorted(tokens, key=get_token_sorting_key)

def sorted_groups(groups):
    return sorted(groups, key=get_group_sorting_key)

def get_token_sorting_key(token):
    groups = [g.id for g in token.groups.all()]
    identity = ''.join([str(1 - groups.count(i)) for i in GROUP_PRIORITY])    # Sort by identity first
    name = token.name
    return ''.join((identity, name))

def get_group_sorting_key(group):
    try:
        return GROUP_PRIORITY.index(group.id)
    except ValueError:
        return len(GROUP_PRIORITY)

def sorted_categories():
    return { category : sorted_groups(category.groups.all()) for category in GroupCategory.objects.all() }

def split_trim_pad(num, *data):
    data = tuple([x.strip() for x in datum.split('\n')] for datum in data)
    num = max(max(map(len, data)), num)
    pad = lambda l, num=num: l + [''] * (num - len(l))
    return tuple(map(pad, data))
