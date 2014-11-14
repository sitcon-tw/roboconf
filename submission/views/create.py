from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect
from submission.forms import SubmissionForm
from core.formatting import render_document
from docs.node import Node

@login_required
def create(request):
	context = {
			'user': request.user,
			'rule': render_document(Node(nid=settings.SUBMISSION_RULE_DOCID).model.current_revision.text.text)
			}

	if request.POST.get('submit'):
		sub = SubmissionForm(request.POST)

		if sub.is_valid():
			submission = sub.save(commit=False)
			submission.user = request.user
			submission.save()
			return redirect('submission:list')
		else:
			pass

	return render(request, 'submission/create.html', context)

# vim: noet ts=8 sw=8
