from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render as render_request
from django.utils.timezone import now
from django.views.decorators.clickjacking import xframe_options_exempt
from docs.models import BlobText, Permalink
from docs.node import Node

@xframe_options_exempt
def render(request, identifier):
	try:
		node = Node(identifier, user=request.user)
	except ObjectDoesNotExist:
		node = None

	if not node or not node.is_file():
		try:
			permalink = Permalink.objects.get(name=identifier)
		except Permalink.DoesNotExist:
			permalink = None

		if not permalink or (permalink.valid_since and permalink.valid_since > now()):
			from django.http import Http404
			raise Http404

		node = Node(nodeobj=permalink.file, user=request.user)
		rev = permalink.revision if permalink.revision else permalink.file.current_revision

	else:
		rev = node.model.current_revision

	if not node.can_view():
		if request.user.is_authenticated():
			from django.core.exceptions import PermissionDenied
			raise PermissionDenied
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

	return render_request(request, 'docs/render.html', {
		'node': node,
		'text': rendered_text,
	})
