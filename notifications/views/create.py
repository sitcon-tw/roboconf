from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from notifications.utils import format_address, parse_address, send_template_mail

@permission_required('notifications.add_message')
def create(request):
    context = {}

    if request.POST.get('submit'):

        if request.POST.get('method') == 'sms':
            pass

        sender = ''
        receivers = {}

        if request.POST.get('sender_email'):
            sender = format_address(request.POST.get('sender_name'), request.POST.get('sender_email'))

        receiver_target = request.POST.get('receiver', '').split(',')
        if 'staff' in receiver_target:
            for user in User.objects.exclude(email='', is_active=False):
                receivers[user.email] = user.profile.name

        if request.POST.get('receivers'):
            additional_receivers = request.POST.get('receivers').strip().split('\n')
            for entry in additional_receivers:
                if ':' in entry:
                    name, addr = parse_address(entry)
                    receivers[addr] = name
                else:
                    receivers[entry] = ''

        # TODO: Reimplement batch sending
        for email, name in receivers.iteritems():
            send_template_mail(
                sender,
                format_address(name, email),
                'mail/notification_general.html',
                {
                    'subject': request.POST.get('subject'),
                    'content': request.POST.get('content'),
                    'reply_to': request.POST.get('reply_address'),
                }
            )

        context['status'] = 'success'

    return render(request, 'notifications/create.html', context)
