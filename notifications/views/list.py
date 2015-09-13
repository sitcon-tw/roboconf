from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from notifications.models import Message

@permission_required('notifications.add_message')
def list(request):
    context = {
        'messages': Message.objects.filter(is_sent=False),
    }
    return render(request, 'notifications/list.html', context)
