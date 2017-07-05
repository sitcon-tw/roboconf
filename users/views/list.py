from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.api.decorators import api_endpoint, ajax_required
from core.api.views import render_json
from users.utils import sorted_users, sorted_categories, sorted_groups
from users.models import GroupCategory
from django.db.models.fields import BooleanField
from collections import OrderedDict

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
    teams = sorted_groups(GroupCategory.objects.get(id=settings.TEAM_GROUPCAT_ID).groups.all())

    for i, user in enumerate(users):
        privileged = request.user.has_perm('auth.change_user')
        users[i] = (user, privileged, user.groups.filter(id__in=GroupCategory.objects.get(id=settings.TEAM_GROUPCAT_ID).groups.all()))

    return render(request, 'users/list.html', {
        'users': users,
        'query_string': request.META["QUERY_STRING"],
        'teamleader': len(request.user.profile.lead_team.all()) > 0,
        'categories': sorted_categories,
        'teams': teams,
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
        privileged = request.user.has_perm('auth.change_user') or user.groups.filter(pk__in=request.user.profile.lead_team.all()).exists()
        same_team = any([user.groups.filter(pk__in=team_list).filter(pk=k.id).exists() for k in request.user.groups.filter(pk__in=team_list)])
        allow_phone = privileged or same_team or len(user.profile.lead_team.all())
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

    filters = request.GET.getlist('find')
    groups = request.GET.get('g')
    authorized = request.user.profile.is_authorized()
    trusted = request.user.profile.is_trusted()
    users = apply_filter(filters=filters, groups=groups, trusted=trusted)
    team_list = [x.id for x in GroupCategory.objects.get(pk=settings.TEAM_GROUPCAT_ID).groups.all()]

    users_output = []
    for user in sorted_users(users):
        privileged = request.user.has_perm('auth.change_user')
        sensitive = user == request.user or request.user.has_perm('auth.change_user')
        same_team = any([user.groups.filter(pk__in=team_list).filter(pk=k.id).exists() for k in request.user.groups.filter(pk__in=team_list)])
        allow_phone = privileged or same_team or user.groups.filter(pk__in=settings.TEAM_SUBLEADER_GROUP_IDS)

        entity = OrderedDict()
        entity['id'] = user.id
        entity['username'] = user.username
        entity['groups'] = ','.join([str(g.name) for g in user.groups.all()])
        entity['email'] = user.email
        entity['display_name'] = user.profile.display_name
        entity['title'] = user.profile.title
        entity['last_name'] = user.last_name if privileged else ""
        entity['first_name'] = user.first_name if privileged else ""
        entity['organization'] = user.profile.organization
        entity['avatar'] = user.profile.avatar if "gravatar" in user.profile.avatar else settings.SITE_URL + user.profile.avatar
        entity['phone'] = user.profile.phone if allow_phone else ""
        entity['redmine'] = user.profile.redmine
        entity['slack'] = user.profile.slack
        entity['twenty'] = ("TRUE" if user.profile.twenty else "FALSE") if privileged else ""
        entity['certificate'] = ("TRUE" if user.profile.certificate else "FALSE") if privileged else ""
        entity['cel_dinner'] = ("TRUE" if user.profile.cel_dinner else "FALSE") if privileged else ""
        entity['prev_worker'] = ("TRUE" if user.profile.prev_worker else "FALSE") if privileged else ""
        entity['residence'] = user.profile.residence if privileged else ""
        entity['shirt_size'] = user.profile.shirt_size if privileged else ""
        entity['diet'] = user.profile.diet if privileged else ""
        entity['transportation_aid'] = ("TRUE" if user.profile.transportation_aid else "FALSE") if privileged else ""
        entity['transportation_hr'] = ("TRUE" if user.profile.transportation_hr else "FALSE") if privileged else ""
        entity['transportation'] = user.profile.transportation if privileged else ""
        entity['transportation_fee'] = user.profile.transportation_fee if privileged else ""
        entity['accom'] = ({0: "FALSE", 2: "TRUE", 1: "Either"}.get(user.profile.accom)) if privileged else ""
        entity['roommate'] = user.profile.roommate if privileged else ""
        entity['gender'] = ({1: "Male", 2: "Female", 9: "Other"}.get(user.profile.gender)) if privileged else ""
        #entity['personal_id'] = user.profile.personal_id if sensitive else ("<" + str(len(user.profile.personal_id)) + ">" if privileged else "")
        entity['volunteering_proof'] = ("TRUE" if user.profile.volunteering_proof else "FALSE") if privileged else ""
        entity['volunteering_work_done'] = user.profile.volunteering_work_done if privileged else ""
        entity['volunteering_duration'] = user.profile.volunteering_duration if privileged else ""
        entity['volunteering_time'] = user.profile.volunteering_time if privileged else ""
        entity['birthday'] = user.profile.birthday if sensitive else ("<" + str(len(user.profile.birthday)) + ">" if privileged else "")
        try:
            languages = [f.verbose_name for f in user.profile.language._meta.fields if type(f) == BooleanField and getattr(user.profile.language, f.name)]
            entity['language'] = ",".join((languages + [user.profile.language.other]) if user.profile.language.other else languages)
        except AttributeError:
            entity['language'] = ""
        try:
            abilitiess = [f.verbose_name for f in user.profile.abilities._meta.fields if type(f) == BooleanField and getattr(user.profile.abilities, f.name)]
            entity['abilities'] = ",".join((abilitiess + [user.profile.abilities.other]) if user.profile.abilities.other else abilitiess)
        except AttributeError:
            entity['abilities'] = ""
        entity['bio'] = user.profile.bio
        entity['comment'] = user.profile.comment if privileged else ""

        users_output.append(entity)

    content_type, template = formats[format or 'html']
    return render(request, template, { 'users': users_output }, content_type=content_type)
