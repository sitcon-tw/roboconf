# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import validate_email
from django.db.models.fields import BooleanField
from django.conf import settings
from core.imaging import resize_image
from users.models import *
from users.utils import *

@login_required
def edit(request, username):
    user = get_object_or_404(User, username=username)
    privileged = request.user.has_perm('auth.change_user') or user.groups.filter(pk=request.user.profile.lead_team_id).exists()

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
        if privileged:
            profile.title = request.POST.get('title')

            groups = request.POST.getlist('groups')
            old_groups = user.groups.all()
            for group in old_groups:
                if group.id not in groups:
                    user.groups.remove(group)
            for group_id in groups:
                try:
                    if group_id not in old_groups:
                        user.groups.add(Group.objects.get(id=group_id))
                except GroupDoesNotExist: pass

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        if request.POST.get('gender'):
            profile.gender = int(request.POST.get('gender'))
        profile.twenty = False if request.POST.get('twenty') == 'False' else True
        profile.personal_id = request.POST.get('personal_id')
        profile.school = request.POST.get('school')
        profile.grade = request.POST.get('grade')
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

    if status == 'success':
        render_template_url = 'users/edit_profile.html'
        return render(request, render_template_url, {
            'u': user,
            'privileged': privileged,
            'categories': sorted_categories if privileged else None,
            'options': {
                'residence': settings.RESIDENCE_OPTIONS,
                'shirt_size': settings.SHIRT_SIZE_OPTIONS,
                'diet': settings.DIET_OPTIONS,
                'accom': [(0, '不需要'), (1, '皆可'), (2, '需要')],
                'gender': [(1, '男'), (2, '女'), (9, '其他')],
                'roommate': [(r.id, r.profile.title + " " + r.profile.display_name + " (" + r.username + ")") for r in User.objects.filter(groups=settings.STAFF_GROUP_ID).exclude(id=user.id)],
                'language': [(f.name, f.verbose_name, getattr(user.profile.language, f.name)) for f in language._meta.fields if type(f) == BooleanField],
                'abilities': [(f.name, f.verbose_name, getattr(user.profile.abilities, f.name)) for f in abilities._meta.fields if type(f) == BooleanField],
            },
            'status': status,
        })
    else:
        render_template_url = 'users/edit_profile.html'
        return render(request, render_template_url, {
            'u': user,
            'privileged': privileged,
            'categories': sorted_categories if privileged else None,
            'options': {
                'residence': settings.RESIDENCE_OPTIONS,
                'shirt_size': settings.SHIRT_SIZE_OPTIONS,
                'diet': settings.DIET_OPTIONS,
                'accom': [(0, '不需要'), (1, '皆可'), (2, '需要')],
                'gender': [(1, '男'), (2, '女'), (9, '其他')],
                'roommate': [(r.id, r.profile.title + " " + r.profile.display_name + " (" + r.username + ")") for r in User.objects.filter(groups=settings.STAFF_GROUP_ID).exclude(id=user.id)],
                'language': [(f.name, f.verbose_name, getattr(user.profile.language, f.name)) for f in language._meta.fields if type(f) == BooleanField],
                'abilities': [(f.name, f.verbose_name, getattr(user.profile.abilities, f.name)) for f in abilities._meta.fields if type(f) == BooleanField],
            },
            'errors': errors,
            'status': status,
        })
