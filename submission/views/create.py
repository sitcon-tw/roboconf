from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from submission.models import Submission
from core.formatting import render_document
from docs.node import Node
from django.conf import settings

@login_required
def create(request):
	context = {
			'user': request.user,
			'rule': render_document(Node(nid=settings.SUBMISSION_RULE_DOCID).model.current_revision.text.text)
			}

	if request.POST.get('submit'):
		sub = Submission()
		sub.user = request.user

	return render(request, 'submission/create.html', context)
