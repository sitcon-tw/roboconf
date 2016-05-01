import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import dateparse
from notifications.utils import format_address, send_template_mail, send_template_sms

def send_mail(sender, receiver, template_name, context):
    context['sender'] = sender
    context['receiver'] = receiver
    sender = settings.USER_ISSUE_SENDER.format(sender.profile.name)
    if isinstance(receiver, User):
        receiver = format_address(receiver.profile.name, receiver.email)
    return send_template_mail(sender, receiver, template_name, context)

def send_sms(sender, receiver, template_name, context):
    context['sender'] = sender
    context['receiver'] = receiver
    return send_template_sms('', receiver.profile.phone, template_name, context)

def parse_date(value):
    if len(value) <= 10:
        value = dateparse.parse_date(value)
        if value:
            value = datetime.datetime.combine(value, settings.ISSUE_DEFAULT_DAYTIME)
    else:
        value = dateparse.parse_datetime(value)
    return value

def is_issue_urgent(issue):
    return issue.labels.filter(id=settings.URGENT_ISSUE_ID).exists()
