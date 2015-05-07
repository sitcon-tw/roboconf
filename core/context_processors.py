from django.conf import settings

def site_url(request):
    return {
        'site_url': settings.SITE_URL,
        'site_name': settings.SITE_NAME,
        'site_title': settings.SITE_TITLE,
    }
