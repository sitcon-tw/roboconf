from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from core.api import *
from docs.models import File, Folder, Permission, BlobText
from docs.perms import get_perms, has_perm, optimized_get_perms
from docs.utils import parse_nid
from itertools import chain

@login_required
def main(request):
	from docs.utils import get_nid
	return redirect(reverse('docs:view', args=(get_nid(Folder, 0),)))

def view(request, nidb64):
	f = parse_nid(nidb64)
	if not f:
		from django.http import Http404
		raise Http404

	if request.method == 'POST':
		return post(request, f)
	elif request.method == 'PUT':
		return put(request, f)
	elif request.method == 'DELETE':
		return delete(request, f)
	elif request.is_ajax():
		return not_allowed(request, ['GET', 'POST', 'PUT', 'DELETE'])

	if not has_perm(request.user, f, Permission.VIEW):
		if not request.user.is_authenticated():
			from django.contrib.auth.views import redirect_to_login
			return redirect_to_login(request.path)
		else:
			raise PermissionDenied
	
	if request.is_ajax():
		return get(request, f)
	else:
		perms = get_perms(request.user, f)
		params = {
			'node': f,
			'docperms': {
				'view': True,
				'comment': Permission.COMMENT in perms,
				'edit': Permission.EDIT in perms,
			},
		}

		if isinstance(f, Folder):
			if f.parent:
				params['docperms']['view_parent'] = has_perm(request.user, f.parent, Permission.VIEW)

			nodes = chain(f.folders.all(), f.files.all())
			items = []
			for item in nodes:
				item_perms = optimized_get_perms(request.user, item, f)
				if Permission.VIEW in item_perms:
					items.append({
						'node': item,
						'type': 'folder' if isinstance(item, Folder) else 'file', 
						'starred': item.starring.filter(id=request.user.id).exists(), 
						'docperms': {
							'view': True,
							'comment': Permission.COMMENT in item_perms,
							'edit': Permission.EDIT in item_perms,
						},
					})

			params['items'] = items

			return render(request, 'docs/folder.html', params)
		else:
			return render(request, 'docs/file.html', params)

def get(request, f):
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
			result['author'] = rev.user.username if rev.user else None
			result['content'] = rev.text.text
			result['format'] = dict(BlobText.FORMAT_ENUMERATION).get(rev.text.format)
		elif isinstance(f, Folder):
			items = chain(f.folders.all(), f.files.all())
			result['content'] = [i.nid() for i in items]

	if 'revisions' in details:
		if isinstance(f, File):
			result['revisions'] = [r.id for r in f.revisions.all()]

	if 'permissions' in details:
		effects = dict(Permission.EFFECT_ENUMERATION)
		kinds = dict(Permission.TYPE_ENUMERATION)
		scopes = dict(Permission.SCOPE_ENUMERATION)

		perms = []
		for p in f.permissions.all():
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

def post(request, f):
	if not has_perm(request.user, f, Permission.EDIT):
		raise PermissionDenied

	if f.is_archived:
		return bad_request(request, {'error': 'node_archived'})

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
			return redirect(reverse('docs:view'), args=(f.nid(),))

def put(request, f):
	PUT = parse_json(request)
	if not PUT:
		return bad_request(request, {'error': 'invalid_json'})

	perms = get_perms(request.user, f)

	if 'star' in PUT:
		if not Permission.VIEW in perms: raise PermissionDenied
		if not request.user.is_authenticated():
			return bad_request(request, {'error': 'login_required'})

		f.starring.add(request.user)

	elif 'unstar' in PUT:
		if not Permission.VIEW in perms: raise PermissionDenied
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
		
		parent = parse_nid(PUT.get('at'))
		if not (parent and isinstance(parent, Folder)):
			return bad_request(request, {'error': 'invalid_node'})
		if not has_perm(request.user, parent, Permission.EDIT):
			raise PermissionDenied
		if parent.is_archived:
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
		if not Permission.EDIT in perms: raise PermissionDenied
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

def delete(request, f):
	if not has_perm(request.user, f, Permission.EDIT):
		raise PermissionDenied

	# Remove any possible viewing permission, move to trash can
	f.permissions.clear()
	f.parent = Folder.objects.get(id=-1)
	f.save()

	return render_json(request, {'status': 'success'})
