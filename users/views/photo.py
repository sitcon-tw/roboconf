import re
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.template import Context, Template
from core.api.decorators import api_endpoint
from users.models import UserProfile

def custom_size_raw(request, username, width, height):
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

    s = '''
        {% load imagekit %}

        {% thumbnail size image %}
        '''

    t = Template(s)
    c = Context(context)
    url = re.search(r"src=\"(.*?)\"", t.render(c)).groups()[0]

    return redirect(url)

def custom_size_html(request, username, width, height):
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
    return custom_size_raw(request, username, 400, 400)

@api_endpoint(public=True)
def small(request, username):
    return custom_size_raw(request, username, 100, 100)
