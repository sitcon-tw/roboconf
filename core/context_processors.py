from django.conf import settings

def site_url(request):
    return {
        'site': {
            'url': settings.SITE_URL,
            'name': settings.SITE_NAME,
            'title': settings.SITE_TITLE,
            'email': settings.BROADCAST_EMAIL,
        }
    }
