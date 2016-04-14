from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from users.models import RegisterToken, UserProfile
from users.utils import sorted_users, sorted_tokens, sorted_categories
from users.forms import RegisterForm, TokenEditForm


@login_required
def reg_list_token(request):
    if not request.user.profile.is_authorized() and not request.user.profile.is_trusted():
        return redirect('index')

    filters = request.GET.getlist('find')
    groups = request.GET.get('g')
    tokens = apply_filter(filters=filters, groups=groups)

    return render(request, 'users/reg_list_token.html', {
        'tokens': sorted_tokens(tokens),
        'categories': sorted_categories,
        'filters': filters,
        'params': request.GET.urlencode(),
    })


@login_required
@permission_required('auth.add_user')
def reg_add_token(request):
    if not request.user.profile.is_authorized() and not request.user.profile.is_trusted():
        return redirect('index')
    status = ''

    if 'submit' in request.POST:
        pad = lambda l, n: l + [''] * (n - len(l))

        number = int(request.POST.get('number'))
        title = request.POST.get('title')
        usernames = pad(request.POST.get('usernames').split(","), number)
        emails = pad(request.POST.get('emails').split(","), number)
        display_names = pad(request.POST.get('display_names').split(","), number)
        for tn in range(0, number):
            token = RegisterToken()
            token.title = title
            token.username = usernames[tn]
            token.email = emails[tn]
            token.display_name = display_names[tn]
            token.save()

            for group_id in request.POST.getlist('groups'):
                try:
                    token.groups.add(Group.objects.get(id=int(group_id)))
                except Group.DoesNotExist:
                    pass
                except ValueError:
                    pass
            token.save()

            if request.POST.get('send_email'):
                send_template_mail(settings.DEFAULT_ACCOUNTS_SENDER, format_address(token.name, token.email), 'mail/reg_invitation.html', {'receiver': token})

    return render(request, 'users/reg_add_token.html', {
        'categories': sorted_categories,
        'status': status,
    })


@login_required
@permission_required('auth.add_user')
def reg_edit_token(request, token=None):
    if not request.user.profile.is_authorized() and not request.user.profile.is_trusted():
        return redirect('index')

    status, obj = check_token_status(request, token)
    if not status:
        return obj  # Retuen a template
    reg_token = obj

    if request.method == 'POST':
        form = TokenEditForm(request.POST, instance=reg_token)
        if form.is_valid():
            form.save()
            return redirect('users:reg_list_token')
        else:
            print("error")

    return render(request, 'users/reg_edit_token.html', {
        'categories': sorted_categories,
        "token": reg_token,
    })


def reg_form(request, token=None):
    status, obj = check_token_status(request, token)
    if not status:
        return obj  # Retuen a template
    reg_token = obj

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form.instance.backend = 'django.contrib.auth.backends.ModelBackend'
        if form.is_valid():
            with transaction.atomic():
                form.save()
                reg_token.valid = False
                reg_token.user = form.instance
                reg_token.save()

                u = User()
                u = form.instance
                u.profile.title = reg_token.title
                u.profile.display_name = reg_token.display_name
                u.save()
                u.profile.save()
                for g in reg_token.groups.all():
                    g.user_set.add(form.instance)
            if settings.CODE_FOR_REG_NOTIFICATION:
                exec(settings.CODE_FOR_REG_NOTIFICATION)
            login(request, form.instance)
            return redirect('users:edit', username=form.instance.username)

    try:
        error = form.errors
    except UnboundLocalError:
        error = None

    return render(request, 'users/reg_form.html', {
        "token": token,
        "obj": reg_token,
        "error": error,
    })


def apply_filter(filters, groups, tokens=None):
    tokens = tokens or RegisterToken.objects.all()

    if 'disabled' in filters:
        tokens = tokens.filter(valid=False)
    elif 'all' not in filters:
        tokens = tokens.filter(valid=True)

    if groups:
        to_include, to_exclude = [], []
        for g in groups.split(','):
            try:
                g = int(g)
            except ValueError:
                pass
            else:
                filters.append(g)
                if g >= 0:
                    to_include.append(g)
                else:
                    to_exclude.append(-g)

        if to_include:
            tokens = tokens.filter(groups__in=to_include)

        if to_exclude:
            tokens = tokens.exclude(groups__in=to_exclude)

    return tokens


def check_token_status(request, token):
    try:
        reg_token = RegisterToken.objects.get(token=token)
        if not reg_token.valid:
            return (False, render(request, 'users/reg_form.html', {
                "token": token,
                "error_token": "used_token",
            }))
    except ObjectDoesNotExist:
        return (False, render(request, 'users/reg_form.html', {
            "token": token,
            "error_token": "invalid_token",
        }))
    return (True, reg_token)
