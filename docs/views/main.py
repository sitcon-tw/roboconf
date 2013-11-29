from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from core.api import *
from docs.models import Permission, BlobText
from docs.node import Node

@login_required
def main(request):
	from docs.models import Folder
	node = Node(nodeobj=Folder.objects.get(id=0))
	return redirect(reverse('docs:view', args=(node.nid(),)))

def view(request, nidb64):
	try:
		node = Node(nidb64, user=request.user)
	except ObjectDoesNotExist:
		from django.http import Http404
		raise Http404

	if request.method == 'POST':
		return post(request, node)
	elif request.method == 'PUT':
		return put(request, node)
	elif request.method == 'DELETE':
		return delete(request, node)
	elif request.method != 'GET':
		return not_allowed(request, ['GET', 'POST', 'PUT', 'DELETE'])

	if not node.can_view():
		if not request.user.is_authenticated():
			from django.contrib.auth.views import redirect_to_login
			return redirect_to_login(request.path)
		else:
			raise PermissionDenied
	
	if request.is_ajax():
		return get(request, node)
	else:
		params = { 'node': node }
		if node.is_folder():
			return render(request, 'docs/folder.html', params)
		else:
			return render(request, 'docs/file.html', params)

def get(request, node):
	details = request.GET.getlist('details', ['node'])
	result = {'status': 'success'}

	if 'node' in details:
		result['name'] = node.name
		result['parent'] = node.parent().nid()
		result['modified'] = node.last_modified().isoformat()
		result['archived'] = node.is_archived()
		result['starred'] = node.starred()

	if 'content' in details:
		if node.is_file():
			rev = node.model.current_revision
			result['revision'] = rev.id
			result['author'] = rev.user.username if rev.user else None
			result['content'] = rev.text.text
			result['format'] = dict(BlobText.FORMAT_ENUMERATION).get(rev.text.format)
		elif node.is_folder():
			result['content'] = [i.nid() for i in node.items()]

	if 'revisions' in details:
		if node.is_file():
			result['revisions'] = [r.id for r in node.model.revisions.all()]

	if 'permissions' in details:
		effects = dict(Permission.EFFECT_ENUMERATION)
		kinds = dict(Permission.TYPE_ENUMERATION)
		scopes = dict(Permission.SCOPE_ENUMERATION)

		perms = []
		for p in node.__acl():
			obj = {
				'effect': effects.get(p.effect),
				'type': kinds.get(p.type),
			}

			if p.scope == Permission.PER_GROUP:
				obj['group'] = p.target
			elif p.scope == Permission.PER_USER:
				obj['user'] = p.target
			else:
				obj['scope'] = scopes.get(p.scope)

			perms.append(obj)

		result['permissions'] = perms

	return render_json(request, result)

def post(request, node):
	if not node.can_edit():
		raise PermissionDenied

	if node.is_archived():
		return bad_request(request, {'error': 'node_archived'})

	f = node.model

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
			return redirect(reverse('docs:view'), args=(node.nid(),))

def put(request, f):
	PUT = parse_json(request)
	if not PUT:
		return bad_request(request, {'error': 'invalid_json'})

	f = node.model
	if 'star' in PUT:
		if not node.can_view(): raise PermissionDenied
		if not request.user.is_authenticated():
			return bad_request(request, {'error': 'login_required'})

		f.starring.add(request.user)

	elif 'unstar' in PUT:
		if not node.can_view(): raise PermissionDenied
		if not request.user.is_authenticated():
			return bad_request(request, {'error': 'login_required'})

		f.starring.remove(request.user)

	elif 'rename' in PUT:
		if not Permission.EDIT in perms: raise PermissionDenied
		
		name = PUT.get('name')
		if not name:
			return bad_request(request, {'error': 'invalid_name'})
		f.name = name
		f.save()

	elif 'move' in PUT:
		if not Permission.EDIT in perms: raise PermissionDenied
		
		try:
			parent = Node(PUT.get('at'))

		except ObjectDoesNotExist:
			return bad_request(request, {'error': 'invalid_node'})

		if not parent.is_folder():
			return bad_request(request, {'error': 'node_is_not_a_folder'})

		elif not parent.can_edit():
			raise PermissionDenied

		elif parent.is_archived():
			return bad_request(request, {'error': 'node_archived'})

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
		if node.can_edit(): raise PermissionDenied
		if not request.user.is_authenticated():
			return bad_request(request, {'error': 'login_required'})
		try:
			effects = dict((y, x) for x, y in Permission.EFFECT_ENUMERATION)
			kinds = dict((y, x) for x, y in Permission.TYPE_ENUMERATION)
			scopes = dict((y, x) for x, y in Permission.SCOPE_ENUMERATION)

			perms = []
			for obj in PUT.get('permissions'):
				p = Permission()
				p.effect = effects[obj['effect']]
				p.type = kinds[obj['type']]

				if 'group' in obj:
					p.scope = Permission.PER_GROUP
					p.target = obj['group']
				elif 'user' in obj:
					p.scope = Permission.PER_USER
					p.target = obj['user']
				else:
					p.scope = scopes[obj['scope']]

				perms.append(p)

			f.permissions.clear()
			f.permissions.bulk_create(perms)

		except TypeError:
			return bad_request(request, {'error': 'invalid_permissions'})

		except (KeyError, ValueError):
			return bad_request(request, {'error': 'invalid_entry'})

	return render_json(request, {'status': 'success'})

def delete(request, node):
	if not node.can_edit():
		raise PermissionDenied

	# Remove any possible viewing permission, move to trash can
	f = node.model
	f.permissions.clear()
	f.parent = Folder.objects.get(id=-1)
	f.save()

	return render_json(request, {'status': 'success'})
