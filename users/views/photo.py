import re
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.template import Context, Template
from django.views.decorators.cache import cache_page
from core.api.decorators import api_endpoint
from core.imaging import resize_image
from users.models import UserProfile

@cache_page(60 * 60 * 24 * 14)
@api_endpoint(public=True)
def general(request, username_or_pk, size_p=None):
    size = size_p if size_p else 400
    size = int(request.GET.get('size')) if request.GET.get('size') else size
    if re.match(r'\d+', username_or_pk):
        try:
            profile = UserProfile.objects.get(user__pk=username_or_pk)
        except ObjectDoesNotExist:
            raise Http404('User with pk %d not found' % username_or_pk)
    else:
        try:
            profile = UserProfile.objects.get(user__username=username_or_pk)
        except ObjectDoesNotExist:
            raise Http404('User with username %s not found' % username_or_pk)

    if not profile.photo:
        return HttpResponseRedirect(profile.gravatar+'&s='+str(size))

    image_data, mime = resize_image(profile.photo, size=size)
    return HttpResponse(content=image_data, content_type=mime)

@api_endpoint(public=True)
def medium(request, username_or_pk):
    return general(request, username_or_pk, 400)

@api_endpoint(public=True)
def small(request, username_or_pk):
    return general(request, username_or_pk, 100)
