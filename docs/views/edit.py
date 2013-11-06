from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now
from django.http import Http404
from docs.models import File, Permission, Revision, BlobText
from docs.perms import get_perms
from docs.utils import parse_nid

def edit(request, nidb64):
	f = parse_nid(File, nidb64)
	if not f: raise Http404

	if not has_perm(request.user, f, Permission.EDIT):
		if request.user.is_authenticated():
			raise PermissionDenied 	# Access forbidden
		else:
			return redirect(reverse('users:login') + ('?next=%s' % reverse('docs:edit', args=(nidb64,))))

	if request.method == 'POST':
		fname = request.POST.get('name')
		if fname:
			t = BlobText(text=request.POST.get('text'))
			if request.POST.get('is_markdown'):
				t.format = BlobText.MARKDOWN
			t.save()

			r = Revision(file=f, user=request.user)
			r.base_revision = f.current_revision
			r.text = t
			r.save()

			f.name = fname
			f.current_revision = r
			f.last_modified = now()
			f.save()

			status = 'success'
		else: status = 'invalid_name'
		
	else: status = ''

	return render(request, 'docs_edit.html', {
		'file': f,
		'status': status,
	})
