import re
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.template import Context, Template
from core.api.decorators import api_endpoint
from users.models import UserProfile
import re

def custom_size_raw(request, key, width, height):
    if re.match(r'\d+', key):
        try:
            profile = UserProfile.objects.get(user__pk=key)
        except ObjectDoesNotExist:
            raise Http404('User with pk %d not found' % key)
    else:
        try:
            profile = UserProfile.objects.get(user__username=key)
        except ObjectDoesNotExist:
            raise Http404('User with username %s not found' % key)

    # check photo
    if not profile.photo:
        return HttpResponseRedirect(profile.gravatar+'&s='+str(width))

    context = {
        'size': '{}x{}'.format(width, height),
        'image': profile.photo
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
def medium(request, username_or_pk):
    return custom_size_raw(request, username_or_pk, 400, 400)

@api_endpoint(public=True)
def small(request, username_or_pk):
    return custom_size_raw(request, username_or_pk, 100, 100)
