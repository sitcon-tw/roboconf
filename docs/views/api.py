from core.api import *
from docs.models import File, Folder, Permission, BlobText
from docs.utils import parse_nid, generate_nid
from docs.perms import has_perm

def api(request):
	if request.method == 'GET':
		return get(request)
	elif request.method == 'POST':
		return post(request)
	elif request.method == 'PUT':
		return put(request)
	else:
		return not_allowed(request, ['GET', 'POST', 'PUT'])

def get(request):
	f = parse_nid(request.GET.get('nid'))
	if f and has_perm(request.user, f, Permission.VIEW):
		result = {
			'status': 'success',
			'name': f.name,
			'parent': generate_nid(f.parent) if f.parent else None,
			'modified': f.last_modified.isoformat(),
			'archived': f.is_archived,
			'starred': f.starring.filter(id=request.user.id).exists(),
		}

		if isinstance(f, File):
			rev = f.current_revision
			result['revision'] = rev.id
			result['author'] = rev.user.username
			result['content'] = rev.text.text
			result['format'] = 'markdown' if rev.text.format == BlobText.MARKDOWN else 'text'
		elif isinstance(f, Folder):
			from itertools import chain
			children = list(chain(f.folders.all(), f.files.all()))
			result['content'] = children

		return render(request, result)
	else:
		return bad_request(request, {'status': 'invalid_property'})

def post(request):
	return not_implemented(request, {'status': 'not_implemented'})

def put(request):
	return not_implemented(request, {'status': 'not_implemented'})
