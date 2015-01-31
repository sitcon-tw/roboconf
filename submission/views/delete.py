from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import Http404
from submission.models import Submission
from core.settings.base import SUBMISSION_END
import datetime

@login_required
def delete(request):
    if SUBMISSION_END < datetime.datetime.now():
        raise Http404
    submission = Submission.objects.get(id=request.POST['submission_id'])

    if request.user == submission.user:
        for f in submission.files.all():
            f.file.delete()
        submission.delete()

    return redirect('submission:list')
