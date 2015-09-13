import json
from django import http

def parse_json(request):
    try:
        return json.load(request)
    except ValueError:
        return None

def render_json(request, obj):
    result = json.dumps(obj, ensure_ascii=False)
    return http.HttpResponse(result, content_type='application/json')

def bad_request(request, obj=None):
    if request.is_ajax():
        return http.HttpResponseBadRequest(json.dumps(obj), content_type='application/json')
    else:
        from django.http import HttpResponseBadRequest
        from django.template import (loader, Context)
        template = loader.get_template('400.html')
        return HttpResponseBadRequest(template.render(Context(obj)))

def not_authorized(request, obj=None):
    return http.HttpResponse(json.dumps(obj), content_type='application/json', status=401)

def permission_denied(request, obj=None):
    if request.is_ajax():
        return http.HttpResponseForbidden(json.dumps(obj), content_type='application/json')
    else:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

def not_allowed(request, permitted_methods):
    return http.HttpResponseNotAllowed(permitted_methods)

def not_implemented(request, obj=None):
    return http.HttpResponse(json.dumps(obj), content_type='application/json', status=501)
