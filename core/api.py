import json
from django import http

def render(request, obj):
	result = json.dumps(obj)
	return http.HttpResponse(result, content_type='application/json')

def bad_request(request, obj=None):
	if request.is_ajax():
		return http.HttpResponseBadRequest(json.dumps(obj))
	else:
		from core.views import bad_request as friendly_bad_request
		return friendly_bad_request(request)

def not_allowed(request, permitted_methods):
	return http.HttpResponseNotAllowed(permitted_methods)
