from httplib import HTTPConnection, HTTPException
from urllib import urlencode

def post(appname, action, **kwargs):
	conn = HTTPConnection('staff.sitcon.org')
	endpoint = '/%s/api' % appname
	header = {'Content-Type': 'application/x-www-form-urlencoded'}
	
	args = kwargs
	args['action'] = action

	try:
		conn.request('POST', endpoint, urlencode(args), header)
		response = conn.getresponse()
		return response.status, response.reason, response.read()
	finally:
		conn.close()
