from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from docs.models import File, Folder, Revision, Permission, BlobText
from docs.perms import has_perm
from docs.utils import parse_nid

def create(request):
	f = parse_nid(Folder, request.GET.get('folder'))
	if not f: return redirect(reverse('docs:main'))

	if not has_perm(request.user, f, Permission.EDIT):
		if request.user.is_authenticated():
			raise PermissionDenied 	# Access forbidden
		else:
			return redirect(reverse('users:login'))

	if request.method == 'POST':
		name = request.POST.get('name')
		text = request.POST.get('text')
		is_markdown = request.POST.get('is_markdown')

		if name:
			t = BlobText(text=text)
			if is_markdown:
				t.format = BlobText.MARKDOWN
			t.save()

			r = Revision(user=request.user)
			r.base_revision = f.current_revision
			r.text = t
			r.save()

			fil = File(parent=f)
			fil.name = name
			fil.current_revision = r
			f.save()

			status = 'success'
		else:
			status = 'invalid_name'
	else:
		status = ''

	return render(request, 'docs_create.html', {
		'folder': f,
		'status': status,
	})
