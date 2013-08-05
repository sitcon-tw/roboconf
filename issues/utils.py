from notifications.models import *
from notifications.utils import get_setting, send_template_mail, format_address
from users.utils import get_user_name

def send_mail(sender, receiver, template_name, context):
	sender = get_setting('sender', 'issues') % get_user_name(sender)
	receiver = format_address(get_user_name(receiver), receiver.email)
	return send_template_mail(sender, receiver, template_name, context)
