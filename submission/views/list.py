from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from submission.models import Submission

@login_required
def list(request):
    if request.user.has_perm('submission.review'):
        context = {
            'submissions': Submission.objects.all(),
        }
    else:
        context = {
            'submissions': request.user.submissions.all(),
        }
    return render(request, 'submission/list.html', context)
