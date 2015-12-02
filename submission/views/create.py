from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.http import Http404
from submission.forms import SubmissionForm
from submission.forms import SubmissionFileForm
from core.formatting import render_document
from core.settings.base import SUBMISSION_END
from docs.node import Node
import datetime

@permission_required('submission.add_submission')
def create(request):
    if SUBMISSION_END < datetime.datetime.now():
        raise Http404
    context = {
            'user': request.user,
            'rule': render_document(Node(nid=settings.SUBMISSION_RULE_DOCID).model.current_revision.text.text)
            }

    if request.POST.get('submit'):
        sub = SubmissionForm(request.POST, request.FILES)

        if sub.is_valid():
            submission = sub.save(commit=False)
            submission.user = request.user
            submission.save()

            for f in request.FILES.getlist('slide'):
                form = SubmissionFileForm().save(commit=False)
                form.submission = submission
                form.file = f
                form.save()

            return redirect('submission:list')
        else:
            raise ValidationError(sub.errors.as_data())

    return render(request, 'submission/create.html', context)
