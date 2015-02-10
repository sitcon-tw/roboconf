from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from submission.models import Submission
from core.settings.base import SUBMISSION_END
from users.models import UserProfile
import datetime

@login_required
def list(request):
    if request.user.has_perm('submission.review'):
        profilelist=[]
        for p in UserProfile.objects.all():
            if p.has_submission():
                profilelist.append(p)
        
        context = {
            'submissions': Submission.objects.order_by('type', 'id'),
            'user': request.user,
            'submission_end': SUBMISSION_END,
            'submission_review': True,
            'expired': (SUBMISSION_END < datetime.datetime.now() ),
            'submitter_count': len(profilelist),
        }
    else:
        context = {
            'submissions': request.user.submissions.order_by('type', 'id'),
            'user': request.user,
            'submission_end': SUBMISSION_END,
            'submission_review': False,
            'expired': (SUBMISSION_END < datetime.datetime.now() ),
        }
    return render(request, 'submission/list.html', context)
