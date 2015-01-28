from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from submission.models import Submission
from core.settings.base import SUBMISSION_END
import datetime

@login_required
def score(request):
    if request.user.has_perm('submission.review'):
        context = {
            'submissions': Submission.objects.all(),
            'user': request.user,
            'submission_end': SUBMISSION_END,
            'submission_review': True,
            'expired': (SUBMISSION_END < datetime.datetime.now() ),
        }
    else:
        return redirect('submission:list')

    return render(request, 'submission/score.html', context)
