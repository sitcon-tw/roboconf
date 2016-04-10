from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.api.decorators import api_endpoint, ajax_required
from core.api.views import render_json
from users.utils import sorted_users, sorted_categories
from users.models import GroupCategory

formats = {
    'html': ('text/html', 'users/export.html'),
    'csv': ('text/csv', 'users/export.csv'),
    'xml': ('application/xml', 'users/export.xml'),
    'vcard': ('text/vcard', 'users/export.vcf'),
}

def list(request):
    if not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    elif not request.user.profile.is_authorized():
        return redirect('index')

    filters = request.GET.getlist('find')
    groups = request.GET.get('g')
    trusted = request.user.profile.is_trusted()
    users = apply_filter(filters=filters, groups=groups, trusted=trusted)
    users = sorted_users(users)

    for i, user in enumerate(users):
        privileged = request.user.has_perm('auth.change_user') or user.groups.filter(pk=request.user.profile.lead_team_id).exists()
        users[i] = (user, privileged)

    return render(request, 'users/list.html', {
        'users': users,
        'query_string': request.META["QUERY_STRING"],
        'categories': sorted_categories,
        'filters': filters,
        'params': request.GET.urlencode(),
    })

def apply_filter(filters, groups, users=None, trusted=False):
    users = users or User.objects.all()
    if 'disabled' in filters and trusted:
        users = users.filter(is_active=False)
    elif 'all' not in filters or not trusted:
        users = users.filter(is_active=True)

    if 'non_staff' in filters:
        users = users.exclude(groups=settings.STAFF_GROUP_ID)

    if groups:
        to_include, to_exclude = [], []
        for g in groups.split(','):
            try:
                g = int(g)
            except ValueError: pass
            else:
                filters.append(g)
                if g >= 0:
                    to_include.append(g)
                else:
                    to_exclude.append(-g)

        if to_include:
            users = users.filter(groups__in=to_include)

        if to_exclude:
            users = users.exclude(groups__in=to_exclude)

    return users

@api_endpoint(public=True)
@ajax_required(redirect_url='users:list')
def ajax(request):
    return render_json(request, {
        'status': 'success',
        'users': [
            {
                'id': u.username,
                'name': u.profile.name,
                'title': u.profile.title,
                'avatar': u.profile.avatar,
            }
            for u in sorted_users(User.objects.filter(is_active=True, groups=11))
        ],
    })

@login_required
def contacts(request):
    if not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    elif not request.user.profile.is_authorized():
        return redirect('index')

    filters = request.GET.getlist('find')
    groups = request.GET.get('g')
    trusted = request.user.profile.is_trusted()
    users = apply_filter(filters=filters, groups=groups, trusted=trusted)
    users = sorted_users(users)
    team_list = [x.id for x in GroupCategory.objects.get(pk=settings.TEAM_GROUPCAT_ID).groups.all()]

    for i, user in enumerate(users):
        privileged = request.user.has_perm('auth.change_user') or user.groups.filter(pk=request.user.profile.lead_team_id).exists()
        same_team = any([user.groups.filter(pk__in=team_list).filter(pk=k.id).exists() for k in request.user.groups.filter(pk__in=team_list)])
        allow_phone = privileged or same_team or user.groups.filter(pk__in=settings.TEAM_SUBLEADER_GROUP_IDS)
        users[i] = (user, allow_phone)

    return render(request, 'users/contacts.html', {
        'users': users,
        'authorized': request.user.profile.is_authorized(),
        'show_details': request.GET.get('details') and request.user.profile.is_trusted(),
    })

@login_required
def export(request, format=None):
    if format and format not in formats.keys():
        from django.http import Http404
        raise Http404

    if not request.user.has_perm('auth.change_user'):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    filters = request.GET.getlist('find')
    groups = request.GET.get('g')
    authorized = request.user.profile.is_authorized()
    trusted = request.user.profile.is_trusted()
    users = apply_filter(filters=filters, groups=groups, trusted=trusted)

    users_output = []
    for user in sorted_users(users):
        entity = {
            'id': user.username,
            'name': user.profile.name,
            'title': user.profile.title,
            'avatar': user.profile.avatar,
            'email': user.email,
        }

        if authorized:
            entity['phone'] = user.profile.phone

        if trusted:
            entity['model_id'] = user.id
            entity['last_name'] = user.last_name
            entity['first_name'] = user.first_name
            entity['organization'] = user.profile.organization
            entity['residence'] = user.profile.residence
            entity['shirt_size'] = user.profile.shirt_size
            entity['diet'] = user.profile.diet
            entity['bio'] = user.profile.bio or None
            entity['comment'] = user.profile.comment
            entity['groups'] = ' '.join([str(g.id) for g in user.groups.all()])

        users_output.append(entity)

    content_type, template = formats[format or 'html']
    return render(request, template, { 'users': users_output }, content_type=content_type)
