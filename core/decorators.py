import re
from functools import wraps
from django.utils.decorators import available_attrs

DEFAULT_ALLOWED_ORIGIN = re.compile(r'^https?\:\/\/(?:.+?\.)?sitcon\.org')
DEFAULT_ALLOWED_METHODS = ['GET', 'OPTIONS']

def api_endpoint(methods=None, public=False):
	# Decorator function adding origin check
	def decorator(f):
		@wraps(f, assigned=available_attrs(f))
		def inner(request, *args, **kwargs):
			response = f(request, *args, **kwargs)
			if request.is_ajax() and 'Origin' in request.META:
				origin = request.META['Origin']
				if public:
					response['Access-Control-Allow-Origin'] = '*'
				elif DEFAULT_ALLOWED_ORIGIN.match(origin):
					response['Access-Control-Allow-Origin'] = origin

				methods = methods if methods else DEFAULT_ALLOWED_METHODS
				response['Access-Control-Allow-Methods'] = ','.join(methods)
			return response
		return inner
	return decorator
