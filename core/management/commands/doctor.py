from django.core.management.base import NoArgsCommand
from django.conf import settings
from urllib.request import urlopen
from urllib.error import URLError

class Command(NoArgsCommand):
    help = "Monitor site activities periodically."

    def handle_noargs(self, **options):
        for host in settings.ALLOWED_HOSTS:
            try:
                urlopen('http://%s/' % host)
            except URLError:
                # TODO: Send notifications to admin
                pass
