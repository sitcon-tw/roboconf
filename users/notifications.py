# -*- coding: utf-8 -*-
import email, smtplib
import os

def send_mail(user, subject, content):
	message = email.mime.text.MIMEText(content, 'html')
	message['Subject'] = subject

	client = smtplib.SMTP(os.environ['EMAIL_SERVER'], os.environ['EMAIL_PORT'])
	client.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASSWORD'])
	client.sendmail('"SITCON 行政系統" <staff@sitcon.org>',
					'"%s" <%s>' % (user.username, user.email),
					message.as_string())
	client.quit()

def send_sms(user, content):
	# TODO: implement SMS
	pass
