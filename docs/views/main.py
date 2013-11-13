from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from docs.models import File, Folder, Permission
from docs.perms import get_perms
from docs.utils import parse_nid

@login_required
def main(request):
	from docs.utils import get_nid
	return redirect(reverse('docs:view', args=(get_nid(Folder, 0),)))

def view(request, nidb64):
	f = parse_nid(nidb64)
	if not f:
		from django.http import Http404
		raise Http404

	if request.method == 'GET' and request.is_ajax():
		return get(request, f)
	elif request.method == 'POST':
		return post(request, f)
	elif request.method == 'PUT':
		return put(request, f)
	elif request.method == 'DELETE':
		return delete(request, f)

	return render(request, 'docs_view.html', {'node': f})

def get(request, f):
	pass

def post(request, f):
	pass

def put(request, f):
	pass

def delete(request, f):
	pass
