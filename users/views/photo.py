from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from core.api.decorators import api_endpoint
from users.models import UserProfile

def custom_size(request, username, width, height):
    # check user
    user = get_object_or_404(User, username=username)

    # check profile
    profile = get_object_or_404(UserProfile, user=user)

    photo = profile.photo

    # check photo
    if not photo:
        raise Http404

    context = {
        'size': '{}x{}'.format(width, height),
        'image': photo
    }

    return render(request, 'users/photo.html', context)

@api_endpoint(public=True)
def medium(request, username):
    return custom_size(request, username, 400, 400)

@api_endpoint(public=True)
def small(request, username):
    return custom_size(request, username, 100, 100)
