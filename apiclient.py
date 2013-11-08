from httplib import HTTPConnection, HTTPException
from urllib import urlencode

def post(appname, **kwargs):
	conn = HTTPConnection('staff.sitcon.org')
	endpoint = '/%s/api' % appname
	header = {'Content-Type': 'application/x-www-form-urlencoded'}
	
	try:
		conn.request('POST', endpoint, urlencode(kwargs), header)
		response = conn.getresponse()
		return response.status, response.reason, response.read()
	finally:
		conn.close()
