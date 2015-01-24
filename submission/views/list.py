from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from submission.models import Submission
from core.settings.base import SUBMISSION_END
import datetime

@login_required
def list(request):
    if request.user.has_perm('submission.review'):
        context = {
            'submissions': Submission.objects.all(),
            'user': request.user,
            'submission_end': SUBMISSION_END,
            'expired': (SUBMISSION_END < datetime.datetime.now() ),
        }
    else:
        context = {
            'submissions': request.user.submissions.all(),
            'user': request.user,
            'submission_end': SUBMISSION_END,
            'expired': (SUBMISSION_END < datetime.datetime.now() ),
        }
    return render(request, 'submission/list.html', context)
