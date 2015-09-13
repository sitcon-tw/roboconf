from django.core import mail
from django.core.management.base import NoArgsCommand
from notifications.models import Message

class Command(NoArgsCommand):
    help = "Checks and sends messages from notification queue."

    def handle_noargs(self, **options):
        emails = Message.objects.filter(method=Message.EMAIL, is_sent=False)
        if emails.count():
            conn = mail.get_connection()
            conn.open()

            for item in emails.all():
                item.send(connection=conn)

            conn.close()
