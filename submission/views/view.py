from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.conf import settings
from core.formatting import render_document
from submission.models import Submission

@login_required
def view(request, submission_id):
    if request.user.has_perm('submission.review'):
        instance = get_object_or_404(Submission, id=submission_id)
    else:
        instance = get_object_or_404(Submission, id=submission_id, user=request.user)

    context = {
            'submission': instance,
            }

    return render(request, 'submission/view.html', context)

@login_required
def view_partial(request, submission_id):
    if request.user.has_perm('submission.review'):
        instance = get_object_or_404(Submission, id=submission_id)
    else:
        instance = get_object_or_404(Submission, id=submission_id, user=request.user)

    context = {
            'submission': instance,
            }

    return render(request, 'submission/view_partial.html', context)
