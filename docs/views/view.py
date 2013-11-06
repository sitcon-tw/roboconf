from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import Http404
from docs.models import File, Permission, BlobText
from docs.perms import get_perms
from docs.utils import parse_nid
from core.formatting import render_document

def view(request, nidb64):
	f = parse_nid(File, nidb64)
	if not f: raise Http404

	perms = get_perms(request.user, f)
	if Permission.VIEW not in perms:
		if request.user.is_authenticated():
			raise PermissionDenied 	# Access forbidden
		else:
			return redirect(reverse('users:login') + ('?next=%s' % reverse('docs:view', args=(nidb64,))))

	text = f.current_revision.text
	if text.format == BlobText.MARKDOWN:
		rendered_text = render_document(text.text)
	elif text.format == BlobText.HTML:
		rendered_text = text
	else: # text.format == BlobText.TEXT:
		rendered_text = r'<blockquote>%s</blockquote>' % text.text

	return render(request, 'docs_view.html', {
		'file': f,
		'text': rendered_text,
		'docperms': {
			'can_edit': Permission.EDIT in perms,
			'can_comment': Permission.COMMENT in perms,
		},
	})
