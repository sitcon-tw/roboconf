from django.shortcuts import render
from docs.models import File, Permission, BlobText
from docs.perms import get_perms
from docs.utils import parse_nid

def render(request, permalink):
	f = parse_nid(nidb64, File)
	if not f:
		from django.http import Http404
		raise Http404

	perms = get_perms(request.user, f)
	if Permission.VIEW not in perms:
		if request.user.is_authenticated():
			from django.core.exceptions import PermissionDenied
			raise PermissionDenied 	# Access forbidden
		else:
			from django.contrib.auth.views import redirect_to_login
			return redirect_to_login(request.path)

	text = f.current_revision.text
	if text.format == BlobText.MARKDOWN:
		from core.formatting import render_document
		rendered_text = render_document(text.text)
	elif text.format == BlobText.HTML:
		rendered_text = text
	else: # text.format == BlobText.TEXT:
		rendered_text = r'<blockquote>%s</blockquote>' % text.text

	return render(request, 'docs_render.html', {
		'node': f,
		'text': rendered_text,
		'docperms': {
			'edit': Permission.EDIT in perms,
			'comment': Permission.COMMENT in perms,
		},
	})
