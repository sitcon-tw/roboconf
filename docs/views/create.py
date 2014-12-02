from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from core.api.views import *
from docs.models import *
from docs.node import Node

def create(request):
	if request.method == 'POST':
		kind = request.POST.get('type')
		name = request.POST.get('name')
		at = request.POST.get('at')

		if not (kind and name and at):
			return bad_request(request, {'error': 'invalid_args'})

		try:
			parent = Node(at, user=request.user)
		except ObjectDoesNotExist:
			return bad_request(request, {'error': 'invalid_node'})

		if not parent.is_folder():
			return bad_request(request, {'error': 'node_is_not_a_folder'})

		if not parent.can_edit():
			from django.core.exceptions import PermissionDenied
			raise PermissionDenied
		# Warning: removed creation restrictions on <ALLOW * EDIT> folder. Careful.

		if parent.is_archived():
			return bad_request(request, {'error': 'node_archived'})

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

		f.parent = parent.model
		f.name = name
		f.save()

		node = Node(nodeobj=f, user=request.user)

		if request.is_ajax():
			result = {
				'status': 'success',
				'nid': node.nid(),
				'timestamp': f.last_modified,
			}
			if node.is_file():
				result['revision'] = r.id
			return render(request, result)
		else:
			return redirect('docs:view', node.nid())

	elif request.is_ajax():
		return not_allowed(request, ['POST'])

	else:
		try:
			parent = Node(request.GET.get('at'), user=request.user)
		except (TypeError, ObjectDoesNotExist):
			parent = None

		if not parent or not parent.is_folder():
			return redirect('docs:main')

		if not parent.can_edit():
			if not request.user.is_authenticated():
				from django.contrib.auth.views import redirect_to_login
				return redirect_to_login(request.path)
			else:
				from django.core.exceptions import PermissionDenied
				raise PermissionDenied

		return render(request, 'docs/create.html', {'parent': parent})

def create_revision(request):
	content = request.POST.get('content')
	format = request.POST.get('format')

	if content:
		text = BlobText()
		text.text = content
		text.format = dict((y, x) for x, y in BlobText.FORMAT_ENUMERATION).get(format, BlobText.TEXT)
		text.save()

		r = Revision()
		r.text = text
		r.user = request.user if request.user.is_authenticated() else None
		r.type = Revision.EXTERNAL if text.format == 'link' else Revision.LOCAL
		r.comment = request.POST.get('comment', '')
		r.save()

		return r

	return None
