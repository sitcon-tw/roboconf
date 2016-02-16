 # -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.views.decorators.debug import sensitive_variables
from notifications.utils import send_template_mail, format_address
from users.utils import generate_password, sorted_categories
from users.models import UserProfile

@sensitive_variables('password')
@permission_required('auth.add_user')
def create(request):
    errors = []
    status = ''

    if 'submit' in request.POST:
        user = User()

        username = request.POST.get('username')
        if username:
            if User.objects.filter(username=username).count() < 1:
                user.username = username
            else:
                errors += ['username', 'username_already_taken']
        else:
            errors += ['username', 'invalid_username']

        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        email = request.POST.get('email')
        try:
            validate_email(email)

            if User.objects.filter(email=email).count() < 1:
                user.email = email
            else:
                errors += ['email', 'email_already_taken']

        except ValidationError:
            errors += ['email', 'invalid_email']

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        password = generate_password()
        user.set_password(password)

        if len(errors) < 1:
            user.save()

            user.profile.title = request.POST.get('title')
            user.profile.display_name = request.POST.get('display_name')
            user.profile.school = request.POST.get('school')
            user.profile.bio = request.POST.get('bio')
            user.profile.grade = request.POST.get('grade')
            user.profile.phone = request.POST.get('phone')
            user.profile.comment = request.POST.get('comment')
            user.profile.save()

            for group_id in request.POST.getlist('groups'):
                try:
                    user.groups.add(Group.objects.get(id=group_id))
                except Group.DoesNotExist: pass

            user.save()        # Save the groups information

            if request.POST.get('send_welcome_letter'):
                context = {
                    'sender': request.user,
                    'receiver': user,
                    'password': password,
                    'groups': [g.name for g in user.groups.all()],
                }

                sender_address = format_address(request.user.profile.name, request.user.email)
                receiver_address = format_address(user.profile.name, user.email)
                send_template_mail(sender_address, receiver_address, 'mail/user_welcome.html', context)

            status = 'success'
        else:
            status = 'error'

    return render(request, 'users/create.html', {
        'categories': sorted_categories(),
        'errors': errors,
        'status': status,
    })

@sensitive_variables('password')
def submitter_create(request):
    errors = []
    status = ''

    if 'submit' in request.POST:
        user = User()

        username = request.POST.get('username')
        if username:
            if User.objects.filter(username=username).count() < 1:
                user.username = username
            else:
                errors += ['username', 'username_already_taken']
        else:
            errors += ['username', 'invalid_username']

        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        email = request.POST.get('email')
        try:
            validate_email(email)

            if User.objects.filter(email=email).count() < 1:
                user.email = email
            else:
                errors += ['email', 'email_already_taken']

        except ValidationError:
            errors += ['email', 'invalid_email']

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        password = generate_password()
        user.set_password(password)

        if len(errors) < 1:
            user.save()

            try:
                if request.POST.get('gender'):
                    user.profile.gender = int(request.POST.get('gender'))
                user.profile.twenty = False if request.POST.get('twenty') == 'False' else True
                if request.POST.get('personal_id'):
                    user.profile.personal_id = request.POST.get('personal_id')
                if request.POST.get('school'):
                    user.profile.school = request.POST.get('school')
                if request.POST.get('grade'):
                    user.profile.grade = request.POST.get('grade')
                if request.POST.get('phone'):
                    user.profile.phone = request.POST.get('phone')
                if request.POST.get('residence'):
                    user.profile.residence = request.POST.get('residence')
                if request.POST.get('shirt_size'):
                    user.profile.shirt_size = request.POST.get('shirt_size')
                if request.POST.get('diet'):
                    user.profile.diet = request.POST.get('diet')
                user.profile.transportation_aid = False if request.POST.get('transportation_aid') == 'False' else True
                user.profile.transportation_hr = False if request.POST.get('transportation_hr') == 'False' else True
                if request.POST.get('transportation'):
                    user.profile.transportation = request.POST.get('transportation')
                if request.POST.get('transportation_fee'):
                    user.profile.transportation_fee = request.POST.get('transportation_fee')
                if request.POST.get('accom'):
                    user.profile.accom = int(request.POST.get('accom'))
                if request.POST.get('roommate'): user.profile.roommate = User.objects.get(id=request.POST.get('roommate'))
                user.profile.certificate = False if request.POST.get('certificate') == 'False' else True
                user.profile.cel_dinner = False if request.POST.get('cel_dinner') == 'False' else True
                user.profile.prev_worker = False if request.POST.get('prev_worker') == 'False' else True
                user.profile.display_name = request.POST.get('display_name')
                user.profile.school = request.POST.get('school')
                user.profile.bio = request.POST.get('bio')
                user.profile.grade = request.POST.get('grade')
                user.profile.phone = request.POST.get('phone')
                user.profile.photo = request.FILES['photo']
                user.profile.comment = request.POST.get('comment')
                user.profile.title = u'投稿講者'
                user.profile.save()
            except:
                errors += ['invalid_profile']
                user.delete()
                status = 'error'

                return render(request, 'users/submitter_create.html', {
                    'errors': errors,
                    'options': {
                        'residence': settings.RESIDENCE_OPTIONS,
                        'shirt_size': settings.SHIRT_SIZE_OPTIONS,
                        'diet': settings.DIET_OPTIONS,
                        'accom': [(0, u'不需要'), (1, u'皆可'), (2, u'需要')],
                        'gender': [(1, u'男'), (2, u'女'), (9, u'其他')],
                    },
                    'status': status,
                    'saved': request.POST,
                })

            user.groups.add(Group.objects.get(id=settings.SUBMITTER_GROUP_ID))

            context = {
                'sender': request.user,
                'receiver': user,
                'password': password,
            }

            sender_address = settings.SUBMITTER_ACCOUNTS_SENDER
            receiver_address = format_address(user.profile.display_name, user.email)
            send_template_mail(sender_address, receiver_address, 'mail/submitter_welcome.html', context)

            status = 'success'
        else:
            status = 'error'

    if status == 'success':
        return render(request, 'users/login.html', {
            'status': status,
        })
    else:
        return render(request, 'users/submitter_create.html', {
            'errors': errors,
            'options': {
                'residence': settings.RESIDENCE_OPTIONS,
                'shirt_size': settings.SHIRT_SIZE_OPTIONS,
                'diet': settings.DIET_OPTIONS,
                'accom': [(0, u'不需要'), (1, u'皆可'), (2, u'需要')],
                'gender': [(1, u'男'), (2, u'女'), (9, u'其他')],
            },
            'status': status,
            'saved': request.POST,
        })
