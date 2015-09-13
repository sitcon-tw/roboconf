from users.models import *

def generate_password():
    from os import urandom
    from base64 import urlsafe_b64encode
    # Generate a password with length 12
    return urlsafe_b64encode(urandom(8))[:-1]

GROUP_PRIORITY = [3, 1, 6, 7, 5, 8, 4, 9, 2, 14, 19, 20, 15, 13, 18, 12, 11, 10]    # Sort by team lead -> staff -> consultant
def get_user_sorting_key(user):
    groups = [g.id for g in user.groups.all()]
    identity = ''.join([str(1 - groups.count(i)) for i in GROUP_PRIORITY])    # Sort by identity first
    title = user.profile.title.ljust(5)
    name = user.profile.name
    return ''.join((identity, title, name))

def sorted_users(users):
    return sorted(users, key=get_user_sorting_key)

def sorted_groups(groups):
    return sorted(groups, key=get_group_sorting_key)

def get_group_sorting_key(group):
    try:
        return GROUP_PRIORITY.index(group.id)
    except ValueError:
        return len(GROUP_PRIORITY)

def sorted_categories():
    return { category : sorted_groups(category.groups.all()) for category in GroupCategory.objects.all() }
