import json
from urllib import urlencode
from urllib2 import urlopen, URLError
from django.conf import settings

SMS_API_URL = 'https://rest.nexmo.com/sms/json'

SMS_STATUS_SUCCESS = 0
SMS_STATUS_BUSY = 1
SMS_STATUS_OUT_OF_BALANCE = 9

class SmsMessage(object):
	
	from_sender = ''
	to = ''
	text = ''

	def send(self):
		params = {
			'api_key': settings.SMS_API_KEY,
			'api_secret': settings.SMS_API_SECRET, 
			'type': 'text', 
			'from': self.from_sender if self.from_sender else settings.DEFAULT_SMS_SENDER,
			'to': self.to, 
		}

		try:
			self.text.decode('ascii')
			params['text'] = self.text
		except:
			params['type'] = 'unicode'
			params['text'] = unicode(text, 'utf8').encode('utf8')

		url = '%s?%s' % (SMS_API_URL, urlencode(params))

		try:
			buf = urlopen(url)
			response = json.load(buf)

			# Determine status
			for message in response['messages']:
				if message['status'] != SMS_STATUS_SUCCESS:
					return False

		except URLError:
			# Request failed?
			return False

		return True
