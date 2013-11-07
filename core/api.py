'''
Example usage:
```
API_PATTERNS = (
		('add', view, ('num')),
	)

def add(num):
	result = num + 1
	return {'result': result}

def api(request):
	return route(request, API_PATTERNS)
```
'''
import json
from django.http import HttpResponse

def route(request, actions):
	req_action = request.POST.get('action')
	for action, method, params in actions:
		if not req_action == action: continue

		req_params = []
		for p in params:
			if p[-1:] == '*':
				value = request.POST.get(p[:-1])
			else:
				value = request.POST.get(p)
				if not value: continue
		
			req_params.append(value)

		result = method(*req_params)
		return HttpResponse(json.dumps(result), content_type='application/json')

	from views import bad_request
	return bad_request(request)		# 400 due to non-matching actions
