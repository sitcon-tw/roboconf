from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import validate_email
from django.conf import settings
from core.imaging import resize_image
from users.models import *
from users.utils import *

@login_required
def edit(request, username, fancy=False):
    user = get_object_or_404(User, username=username)
    privileged = request.user.has_perm('auth.change_user')

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

    if request.POST.get('submit'):
        profile = None
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=user)

        if privileged and not fancy:
            username = request.POST.get('username')
            if username != user.username:
                if username:
                    if User.objects.filter(username=username).count() < 1:
                        user.username = username
                    else:
                        errors += ['username', 'username_already_taken']
                else:
                    errors += ['username', 'invalid_username']

            groups = request.POST.getlist('groups')
            old_groups = user.groups.all()
            for group in old_groups:
                if group.id not in groups:
                    user.groups.remove(group)

            for group_id in groups:
                try:
                    if group_id not in old_groups:
                        user.groups.add(Group.objects.get(id=group_id))
                except Group.DoesNotExist: pass

            profile.title = request.POST.get('title')

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        if not fancy:
            email = request.POST.get('email', '')
            if email != user.email:
                try:
                    validate_email(email)

                    if User.objects.filter(email=email).count() < 1:
                        user.email = email
                    else:
                        errors += ['email', 'email_already_taken']
                except ValidationError:
                    errors += ['email', 'invalid_email']

        profile.display_name = request.POST.get('display_name')
        profile.school = request.POST.get('school')
        profile.grade = request.POST.get('grade')
        profile.phone = request.POST.get('phone')
        profile.residence = request.POST.get('residence')
        profile.shirt_size = request.POST.get('shirt_size')
        profile.diet = request.POST.get('diet')

        photo = request.FILES.get('photo')
        if photo:
            if photo.size > settings.AVATAR_FILE_SIZE_LIMIT:
                errors += ['photo', 'photo_too_large']
            else:
                try:
                    photo_data = resize_image(photo, size=settings.AVATAR_IMAGE_SIZE_LIMIT)
                    resized_photo = SimpleUploadedFile(name=photo.name, content=photo_data, content_type=photo.content_type)
                    profile.photo = resized_photo
                except ValueError:
                    errors += ['photo', 'photo_invalid']

        profile.bio = request.POST.get('bio')
        profile.comment = request.POST.get('comment')

        if len(errors) < 1:
            user.save()
            profile.save()
            status = 'success'
        else:
            status = 'error'

    if fancy and status == 'success':
        return redirect("index")
    else:
        render_template_url = 'users/edit_profile.html' if not fancy else 'users/fancy_edit_profile.html'
        return render(request, render_template_url, {
            'u': user,
            'categories': sorted_categories if privileged else None,
            'options': {
                'residence': settings.RESIDENCE_OPTIONS,
                'shirt_size': settings.SHIRT_SIZE_OPTIONS,
                'diet': settings.DIET_OPTIONS,
            },
            'errors': errors,
            'status': status,
        })
