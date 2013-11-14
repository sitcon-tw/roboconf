from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from core.api import *
from docs.models import *
from docs.perms import has_perm
from docs.utils import parse_nid

def create(request):
	if request.method == 'POST':
		kind = request.POST.get('type')
		name = request.POST.get('name')
		at = request.POST.get('at')

		if not (kind and name and at):
			return bad_request(request, {'error': 'invalid_args'})

		parent = parse_nid(at)
		if not (parent and isinstance(parent, Folder)):
			return bad_request(request, {'error': 'invalid_node'})

		if not has_perm(request.user, parent, Permission.EDIT):
			from django.core.exceptions import PermissionDenied
			raise PermissionDenied

		if kind == 'file':
			r = create_revision(request)
			if not r:
				return bad_request(request, {'error': 'content_required'})		
			f = File()
			f.current_revision = r
		elif kind == 'folder':
			f = Folder()
		else:
			return bad_request(request, {'error': 'invalid_type'})

		f.parent = parent
		f.name = name
		f.save()

		if request.is_ajax():
			result = {
				'status': 'success',
				'nid': f.nid(),
				'timestamp': f.last_modified,
			}
			if isinstance(f, File):
				result['revision'] = r.id
			return render(request, result)
		else:
			return redirect(reverse('docs:node'), args=(f.nid(),))

	return render(request, 'docs_create.html', {})

def create_revision(request):
	content = request.POST.get('content')
	format = request.POST.get('format')

	if content:
		text = BlobText()
		text.text = content
		text.format = dict((y, x) for x, y in BlobText.FORMAT_ENUMERATION).get('format', BlobText.TEXT)
		text.save()

		r = Revision()
		r.text = text
		r.user = request.user
		r.type = Revision.EXTERNAL if text.format == 'link' else Revision.LOCAL
		r.comment = request.POST.get('comment', '')
		r.save()

		return r
	
	return None