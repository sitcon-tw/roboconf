from django.shortcuts import render as render_request
from docs.models import File, Permission, BlobText, Permalink
from docs.perms import get_perms
from docs.utils import parse_nid

def render(request, identifier):
	f = parse_nid(identifier)

	if not f or not isinstance(f, File):
		try:
			permalink = Permalink.objects.get(name=identifier)
		except Permalink.DoesNotExist:
			pass

		from django.utils.timezone import now
		if not permalink or permalink.valid_since > now():
			from django.http import Http404
			raise Http404

		f = permalink.file
		rev = permalink.revision if permalink.revision else f.current_revision

	else: rev = f.current_revision

	perms = get_perms(request.user, f)
	if Permission.VIEW not in perms:
		if request.user.is_authenticated():
			from django.core.exceptions import PermissionDenied
			raise PermissionDenied 	# Access forbidden
		else:
			from django.contrib.auth.views import redirect_to_login
			return redirect_to_login(request.path)

	text = rev.text
	if text.format == BlobText.MARKDOWN:
		from core.formatting import render_document
		rendered_text = render_document(text.text)
	elif text.format == BlobText.HTML:
		rendered_text = text
	else: # text.format == BlobText.TEXT:
		rendered_text = r'<blockquote>%s</blockquote>' % text.text

	return render_request(request, 'docs_render.html', {
		'node': f,
		'text': rendered_text,
		'docperms': {
			'edit': Permission.EDIT in perms,
			'comment': Permission.COMMENT in perms,
		},
	})
