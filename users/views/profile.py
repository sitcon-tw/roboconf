from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.conf import settings
from core.api.decorators import api_endpoint
from core.api.views import *
from users.models import GroupCategory

@login_required
@api_endpoint(public=True)
def profile(request, username):
    user = get_object_or_404(User, username=username)
    privileged = request.user.has_perm('auth.change_user')

    team_list = GroupCategory.objects.get(pk=settings.TEAM_GROUPCAT_ID).groups.all()
    same_team = any([user.groups.filter(pk__in=team_list).filter(pk=k.id).exists() for k in request.user.groups.filter(pk__in=team_list)])

    if request.is_ajax():
        if user.is_active:
            return render_json(request, {
                'status': 'success',
                'user': {
                    'id': user.username,
                    'name': user.profile.name,
                    'title': user.profile.title,
                    'avatar': user.profile.avatar,
                }
            })
        return bad_request(request, {'status': 'invalid'})

    elif not request.user.is_authenticated():
        return redirect_to_login(request.path)

    return render(request, 'users/profile.html', {
        'u': user,
        'allow_phone': privileged or same_team or len(user.profile.lead_team.all()),
        'sensitive': user == request.user or request.user.has_perm('auth.change_user'),
        'privileged': privileged,
        'teams': filter(lambda x: x in user.groups.all(), team_list),
        'show_detail': user == request.user or privileged or request.user.has_perm('view_profile_detail'),
    })

@login_required
def me(request):
    return redirect('users:profile', request.user.username)
