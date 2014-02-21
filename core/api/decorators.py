from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import available_attrs

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
