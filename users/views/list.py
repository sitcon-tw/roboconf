from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from core.api.decorators import api_endpoint, ajax_required
from core.api.views import render_json
from core.settings.base import PROJECT_PATH
from users.utils import sorted_users, sorted_categories
from submission.models import Submission

import os
import zipfile
import StringIO

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
    submission = request.GET.getlist('submission')
    trusted = request.user.profile.is_trusted()
    users = apply_filter(filters=filters, groups=groups, submission=submission, trusted=trusted)

    return render(request, 'users/list.html', {
        'users': sorted_users(users),
        'categories': sorted_categories,
        'filters': filters,
        'params': request.GET.urlencode(),
    })

def apply_filter(filters, groups, users=None, submission=None, trusted=False):
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

    if 'accepted' in submission:
        _submissions = Submission.objects.filter(status='A')
        _u_pks = [ s.user.pk for s in _submissions ]
        users = users.filter(pk__in=_u_pks)
    elif 'editing' in submission:
        _submissions = Submission.objects.filter(status='E')
        _u_pks = [ s.user.pk for s in _submissions ]
        users = users.filter(pk__in=_u_pks)
    elif 'rejected' in submission:
        _submissions = Submission.objects.filter(status='R')
        _u_pks = [ s.user.pk for s in _submissions ]
        users = users.filter(pk__in=_u_pks)
    elif 'none' in submission:
        users = users.filter(submissions__isnull=True)

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
    return render(request, 'users/contacts.html', {
        'users': sorted_users(User.objects.filter(is_active=True)),
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
    submission = request.GET.getlist('submission')
    authorized = request.user.profile.is_authorized()
    trusted = request.user.profile.is_trusted()
    users = apply_filter(filters=filters, groups=groups, submission=submission, trusted=trusted)

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
            entity['school'] = user.profile.school
            entity['grade'] = user.profile.grade
            entity['residence'] = user.profile.residence
            entity['shirt_size'] = user.profile.shirt_size
            entity['diet'] = user.profile.diet
            entity['bio'] = user.profile.bio or None
            entity['comment'] = user.profile.comment
            entity['groups'] = ' '.join([str(g.id) for g in user.groups.all()])

        users_output.append(entity)

    content_type, template = formats[format or 'html']
    return render(request, template, { 'users': users_output }, content_type=content_type)

@permission_required('users.export_photo')
def export_photo(request):
    filters = request.GET.getlist('find')
    groups = request.GET.get('g')
    submission = request.GET.getlist('submission')
    authorized = request.user.profile.is_authorized()
    trusted = request.user.profile.is_trusted()
    users = apply_filter(filters=filters, groups=groups, submission=submission, trusted=trusted)

    # copied from: https://stackoverflow.com/a/12951461/446391
    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    zip_filename = "profile_photo_export.zip"

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    export_count = 0
    for user in users:
        if user.profile.photo:
            # Calculate path for file in zip
            fdir, fname = os.path.split(user.profile.photo.url)

            # Add file, at correct path
            zf.write(os.path.join(PROJECT_PATH, user.profile.photo.url[1:]), fname)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp
