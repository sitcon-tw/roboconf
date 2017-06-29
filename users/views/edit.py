# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import validate_email
from django.db.models.fields import BooleanField
from django.conf import settings
from core.imaging import resize_image
from users.models import *
from users.utils import *
import json

@login_required
def team(request, username, tid):
    user = get_object_or_404(User, username=username)
    team = get_object_or_404(Group, id=tid)
    privileged = request.user.has_perm('auth.change_user')

    if not (team in request.user.profile.lead_team.all() or privileged):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    errors = []
    status = ''

    if request.POST.get('data') == 'true':
        team.user_set.add(user)
    else:
        team.user_set.remove(user)

    if len(errors) < 1:
        team.save()
        status = 'success'
    else:
        status = 'error'

    if status == 'success':
        return HttpResponse(json.dumps([{'id': g.id, 'name': g.name} for g in GroupCategory.objects.get(id=settings.TEAM_GROUPCAT_ID).groups.filter(id__in=user.groups.all())]), content_type="application/json; charset=utf-8")
    else:
        return HttpResponse(' '.join(errors))

@login_required
def edit(request, username):
    user = get_object_or_404(User, username=username)
    privileged = request.user.has_perm('auth.change_user')
    team_list = sorted_groups(GroupCategory.objects.get(id=settings.TEAM_GROUPCAT_ID).groups.all())
    user_teams = user.groups.filter(id__in=GroupCategory.objects.get(id=settings.TEAM_GROUPCAT_ID).groups.all())

    if not (user == request.user or privileged):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    errors = []
    status = ''

    action = request.POST.get('action')
    if action and privileged:
        if action == 'activate':
            user.is_active = True
        elif action == 'deactivate':
            user.is_active = False
        user.save()
        status = 'success'

    profile = None

    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)

    if not user.profile.language:
        lang = language()
        lang.save()
        user.profile.language = lang
        user.profile.save()

    if not user.profile.abilities:
        abil = abilities()
        abil.save()
        user.profile.abilities = abil
        user.profile.save()

    if request.POST.get('submit'):
        profile.display_name = request.POST.get('display_name')
        if request.user.has_perm('auth.change_user'):
            profile.title = request.POST.get('title')

            lead_teams = request.POST.getlist('lead_teams')
            old_lead_teams = user.profile.lead_team.all()
            for team in old_lead_teams:
                if team.id not in lead_teams:
                    user.profile.lead_team.remove(team)
            for team_id in lead_teams:
                try:
                    if team_id not in old_lead_teams:
                        user.profile.lead_team.add(Group.objects.get(id=team_id))
                except GroupDoesNotExist:
                    pass

            groups = request.POST.getlist('groups')
            old_groups = user.groups.all()
            for group in old_groups:
                if group.id not in groups:
                    user.groups.remove(group)
            for group_id in groups:
                try:
                    if group_id not in old_groups:
                        user.groups.add(Group.objects.get(id=group_id))
                except GroupDoesNotExist:
                    pass

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        if request.POST.get('gender'):
            profile.gender = int(request.POST.get('gender'))
        profile.twenty = False if request.POST.get('twenty') == 'False' else True
        profile.personal_id = request.POST.get('personal_id')
        profile.organization = request.POST.get('organization')
        profile.slack = request.POST.get('slack')
        profile.redmine = request.POST.get('redmine')
        if request.POST.get('phone'):
            profile.phone = request.POST.get('phone')
        if request.POST.get('residence'):
            profile.residence = request.POST.get('residence')
        if request.POST.get('shirt_size'):
            profile.shirt_size = request.POST.get('shirt_size')
        if request.POST.get('diet'):
            profile.diet = request.POST.get('diet')
        profile.transportation_aid = False if request.POST.get('transportation_aid') == 'False' else True
        profile.transportation_hr = False if request.POST.get('transportation_hr') == 'False' else True
        profile.transportation = request.POST.get('transportation')
        profile.transportation_fee = request.POST.get('transportation_fee')
        if request.POST.get('accom'):
            profile.accom = int(request.POST.get('accom'))
        profile.roommate = request.POST.get('roommate')

        profile.volunteering_proof = False if request.POST.get('volunteering_proof') == 'False' else True
        profile.volunteering_duration = request.POST.get('volunteering_duration')
        profile.volunteering_time = request.POST.get('volunteering_time')
        profile.volunteering_work_done = request.POST.get('volunteering_work_done')
        profile.birthday = request.POST.get('birthday')
        profile.certificate = False if request.POST.get('certificate') == 'False' else True
        profile.cel_dinner = False if request.POST.get('cel_dinner') == 'False' else True
        profile.prev_worker = False if request.POST.get('prev_worker') == 'False' else True
        profile.language.other = request.POST.get('language_other')
        profile.abilities.other = request.POST.get('abilities_other')

        photo = request.FILES.get('photo')
        if photo:
            if photo.size > settings.AVATAR_FILE_SIZE_LIMIT:
                errors += ['photo', 'photo_too_large']
            else:
                try:
                    image_data, mime  = resize_image(photo, size=settings.AVATAR_IMAGE_SIZE_LIMIT)
                    resized_photo = SimpleUploadedFile(name=photo.name, content=image_data, content_type=mime)
                    profile.photo = resized_photo
                except ValueError:
                    errors += ['photo', 'photo_invalid']

        data = dict(request.POST.lists())

        try:
            data['language']
        except KeyError:
            for f in [f.name for f in language._meta.fields if type(f) == BooleanField]:
                setattr(user.profile.language, f, False)
        else:
            for f in [f.name for f in language._meta.fields if type(f) == BooleanField]:
                if f not in data['language']:
                    setattr(user.profile.language, f, False)
                else:
                    setattr(user.profile.language, f, True)

        try:
            data['abilities']
        except KeyError:
            for f in [f.name for f in abilities._meta.fields if type(f) == BooleanField]:
                setattr(user.profile.abilities, f, False)
        else:
            for f in [f.name for f in abilities._meta.fields if type(f) == BooleanField]:
                if f not in data['abilities']:
                    setattr(user.profile.abilities, f, False)
                else:
                    setattr(user.profile.abilities, f, True)

        profile.bio = request.POST.get('bio')
        profile.comment = request.POST.get('comment')

        if len(errors) < 1:
            user.save()
            profile.save()
            profile.language.save()
            profile.abilities.save()
            status = 'success'
        else:
            status = 'error'

    render_template_url = 'users/edit_profile.html'
    return render(request, render_template_url, {
        'u': user,
        'privileged': privileged,
        'teamleader': len(user.profile.lead_team.all()) > 0,
        'teams': user_teams,
        'team_list': team_list,
        'sensitive': user == request.user or request.user.has_perm('auth.change_user'),
        'categories': sorted_categories if privileged else None,
        'options': {
            'residence': settings.RESIDENCE_OPTIONS,
            'shirt_size': settings.SHIRT_SIZE_OPTIONS,
            'diet': settings.DIET_OPTIONS,
            'accom': [(0, '不需要'), (1, '皆可'), (2, '需要')],
            'gender': [(1, '男'), (2, '女'), (9, '其他')],
            'language': [(f.name, f.verbose_name, getattr(user.profile.language, f.name)) for f in language._meta.fields if type(f) == BooleanField],
            'abilities': [(f.name, f.verbose_name, getattr(user.profile.abilities, f.name)) for f in abilities._meta.fields if type(f) == BooleanField],
        },
        'status': status,
        'errors': errors
    })
