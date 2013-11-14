from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from core.api import *
from docs.models import File, Folder, Permission, BlobText
from docs.perms import get_perms, has_perm
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
	if not has_perm(request.user, f, Permission.VIEW):
		raise PermissionDenied
	
	details = request.GET.getlist('details', ['node'])
	result = {'status': 'success'}

	if 'node' in details:
		result['name'] = f.name
		result['parent'] = f.parent.nid()
		result['modified'] = f.last_modified.isoformat()
		result['archived'] = f.is_archived
		result['starred'] = f.starring.filter(id=request.user.id).exists()

	if 'content' in details:
		if isinstance(f, File):
			rev = f.current_revision
			result['revision'] = rev.id
			result['author'] = rev.user.username
			result['content'] = rev.text.text
			result['format'] = dict(BlobText.FORMAT_ENUMERATION).get(rev.text.format)
		elif isinstance(f, Folder):
			from itertools import chain
			items = chain(f.folders.all(), f.files.all())
			result['content'] = [i.nid() for i in items]

	if 'revisions' in details:
		if isinstance(f, File):
			result['revisions'] = [r.id for r in f.revisions.all()]

	return render_json(request, result)

def post(request, f):
	if not has_perm(request.user, f, Permission.EDIT):
		raise PermissionDenied
	
	if not request.user.is_authenticated():
		return not_authorized(request, {'error': 'anonymous_edit_not_implemented'})

	from docs.views.create import create_revision
	r = create_revision(request)

	if not r:
		return bad_request(request, {'error': 'content_required'})
	else:
		r.base_revision = f.current_revision
		r.save()

		f.current_revision = r
		f.last_modified = now()
		f.save()

		if request.is_ajax():
			result = {
				'status': 'success',
				'base': r.base_revision.id,
				'current': r.id,
				'timestamp': f.last_modified,
			}
			return render(request, result)
		else:
			return redirect(reverse('docs:node'), args=(f.nid(),))

def put(request, f):
	PUT = parse_json(request)
	if not PUT:
		return bad_request(request, {'error': 'invalid_json'})

	if not request.user.is_authenticated():
		return not_authorized(request, {'error': 'anonymous_edit_not_implemented'})

	perms = get_perms(request.user, f)

	if 'star' in PUT:
		if not Permission.VIEW in perms: raise PermissionDenied
		f.starring.add(request.user)

	elif 'rename' in PUT:
		if not Permission.EDIT in perms: raise PermissionDenied
		name = PUT.get('name')
		if not name:
			return bad_request(request, {'error': 'invalid_name'})
		f.name = name
		f.save()

	elif 'move' in PUT:
		if not Permission.EDIT in perms: raise PermissionDenied
		parent = parse_nid(PUT.get('at'))
		if not (parent and isinstance(parent, Folder)):
			return bad_request(request, {'error': 'invalid_node'})
		f.parent = parent
		f.save()

	elif 'archive' in PUT:
		if not request.user.has_perm('docs.archive'): raise PermissionDenied
		f.is_archived = True
		f.save()

	elif 'unarchive' in PUT:
		if not request.user.has_perm('docs.archive'): raise PermissionDenied
		f.is_archived = False
		f.save()

	elif 'permissions' in PUT:
		if not Permission.EDIT in perms: raise PermissionDenied

		return not_implemented(request, {'error': 'not_implemented'})

	return render_json(request, {'status': 'success'})

def delete(request, f):
	if not has_perm(request.user, f, Permission.EDIT):
		raise PermissionDenied

	if not request.user.is_authenticated():
		return not_authorized(request, {'error': 'anonymous_edit_not_implemented'})

	return not_implemented(request, {'error': 'not_implemented'})
