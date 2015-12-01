from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.conf import settings
from django.http import Http404
from core.formatting import render_document
from docs.node import Node
from submission.forms import SubmissionForm
from submission.forms import SubmissionFileForm
from submission.models import Submission
from core.settings.base import SUBMISSION_END
import datetime


@login_required
def edit(request, submission_id):
    if SUBMISSION_END < datetime.datetime.now():
        instance = get_object_or_404(Submission, id=submission_id, user=request.user)
        if not ( instance.status=='E' or instance.status=='Z' ):
            raise Http404
    else:
        instance = get_object_or_404(Submission, id=submission_id, user=request.user)

    if request.POST.get('submit'):
        if request.FILES:
            submission = SubmissionForm(request.POST, request.FILES, instance=instance)
        else:
            submission = SubmissionForm(request.POST, instance=instance)

        if submission.is_valid():

            sub = submission.save()

            if request.FILES.getlist('slide'):

                for f in sub.files.all():
                    f.file.delete()
                    f.delete()

                for f in request.FILES.getlist('slide'):
                    form = SubmissionFileForm().save(commit=False)
                    form.submission = sub
                    form.file = f
                    form.save()

            return redirect('submission:list')
        else:
            pass

    context = {
            'user': request.user,
            'rule': render_document(Node(nid=settings.SUBMISSION_RULE_DOCID).model.current_revision.text.text),
            'submission': instance,
            }

    return render(request, 'submission/edit.html', context)
