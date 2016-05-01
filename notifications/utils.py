from core.context_processors import site_url
from django.template.loader import render_to_string
from email.utils import formataddr
from notifications.models import Message

def to_email_address(nsaddr):
    return formataddr(parse_address(nsaddr))

def format_address(name, addr):
    return '%s:%s' % (
        str(name if name is not None else '').strip().replace(':', '-'),
        str(addr if addr is not None else '').strip()
    )

def parse_address(nsaddr):
    if nsaddr is None: return ('', '')
    (name, _, addr) = nsaddr.rpartition(':')
    return (name, addr)

'''
Create message from a specific set of context.
'''
def send_template_mail(sender, receiver, template_name, context, autosave=True):
    message = Message()
    message.sender = sender
    message.receiver = receiver

    context['sender_address'] = sender
    context['receiver_address'] = receiver
    context.update(site_url(None))
    raw_content = render_to_string(template_name, context).strip()

    subject, _, content = raw_content.partition('\n=====\n')
    message.subject = subject
    message.content = content
    if autosave:
        message.save()
    return message

def send_template_sms(sender, receiver, template_name, context, autosave=True):
    message = Message()
    message.method = Message.SMS
    message.sender = sender
    message.receiver = receiver

    context['sender_address'] = sender
    context['receiver_address'] = receiver
    context.update(site_url(None))

    content = render_to_string(template_name, context).strip()
    message.content = content
    if autosave:
        message.save()
    return message
