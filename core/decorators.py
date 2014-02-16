import re
from functools import wraps
from django.utils.decorators import available_attrs
from django.http.response import HttpResponse

DEFAULT_ALLOWED_ORIGIN = re.compile(r'^https?\:\/\/(?:.+?\.)?sitcon\.org')
DEFAULT_ALLOWED_METHODS = ['GET', 'OPTIONS']

def api_endpoint(methods=None, public=False):
	# Decorator function adding origin check
	def decorator(f):
		@wraps(f, assigned=available_attrs(f))
		def inner(request, *args, **kwargs):
			response = f(request, *args, **kwargs)
			
			if 'HTTP_ORIGIN' in request.META:
				origin = request.META['HTTP_ORIGIN']

				if request.method == 'OPTIONS':
					response = HttpResponse()	# Reset HTTP response

					methods = methods if methods else DEFAULT_ALLOWED_METHODS
					response['Access-Control-Allow-Methods'] = ','.join(methods)
					response['Access-Control-Allow-Headers'] = ['X-Requested-With']

				if public:
					response['Access-Control-Allow-Origin'] = '*'
				elif DEFAULT_ALLOWED_ORIGIN.match(origin):
					response['Access-Control-Allow-Origin'] = origin

			return response
		return inner
	return decorator
