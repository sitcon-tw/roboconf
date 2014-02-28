from django.conf import settings
from django.views.generic.base import RedirectView

def redirect_static(path):
	return RedirectView.as_view(url=(settings.STATIC_URL + path))