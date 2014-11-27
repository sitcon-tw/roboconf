from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from submission.models import Submission

@login_required
def delete(request):
    submission = Submission.objects.get(id=request.POST['submission_id'])

    if request.user == submission.user:
        for f in submission.files.all():
            f.file.delete()
        submission.delete()

    return redirect('submission:list')
