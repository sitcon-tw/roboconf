from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from docs.models import Folder, Permission
from docs.perms import get_perms
from docs.utils import generate_nid, parse_nid

@login_required
def main(request):
	# Redirect to root folder
	return redirect(reverse('docs:folder', args=(generate_nid(0),)))

def folder(request, nidb64):
	f = parse_nid(Folder, nidb64)
	if not f: raise Http404

	perms = get_perms(request.user, f)
	if Permission.VIEW not in perms:
		if user.is_authenticated():
			raise Http404 	# Access forbidden
		else:
			return redirect(reverse('users:login') + ('?next=%s' % reverse('docs:folder', args=(nidb64,))))

	return render(request, 'docs_folder.html', {
		'folder': f,
		'can_edit': Permission.EDIT in perms,
	})
