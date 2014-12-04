from django.conf import settings

def site_url(request):
    return { 'site_url': settings.SITE_URL }
