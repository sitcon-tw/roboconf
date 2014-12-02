import re
from functools import wraps
from django.shortcuts import redirect
from django.http.response import HttpResponse
from django.utils.decorators import available_attrs

DEFAULT_ALLOWED_ORIGIN = re.compile(r'^https?\:\/\/(?:.+?\.)?sitcon\.org')
DEFAULT_ALLOWED_METHODS = ['GET', 'OPTIONS']
DEFAULT_ALLOWED_HEADERS = ['X-Requested-With']

def api_endpoint(methods=None, public=False):
	# Decorator function for adding origin check
	def decorator(f):
		@wraps(f, assigned=available_attrs(f))
		def inner(request, *args, **kwargs):
			response = f(request, *args, **kwargs)

			if 'HTTP_ORIGIN' in request.META:
				origin = request.META['HTTP_ORIGIN']

				if request.method == 'OPTIONS':
					response = HttpResponse()	# Reset HTTP response

					m = methods if methods else DEFAULT_ALLOWED_METHODS
					response['Access-Control-Allow-Methods'] = ','.join(m)
					response['Access-Control-Allow-Headers'] = ','.join(DEFAULT_ALLOWED_HEADERS)

				if public:
					response['Access-Control-Allow-Origin'] = '*'
				elif DEFAULT_ALLOWED_ORIGIN.match(origin):
					response['Access-Control-Allow-Origin'] = origin

			return response
		return inner
	return decorator

def ajax_required(redirect_url=None):
	# Decorator function for redirecting non-ajax request
	def decorator(f):
		@wraps(f, assigned=available_attrs(f))
		def inner(request, *args, **kwargs):
			if request.is_ajax():
				return f(request, *args, **kwargs)
			else:
				return redirect(redirect_url, permanent=True)
		return inner
	return decorator
