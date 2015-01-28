from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from submission.models import Submission
from submission.forms import ScoreForm
from core.settings.base import SUBMISSION_END
import json
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

@login_required
def score_save(request):
    if request.user.has_perm('submission.review'):

        data = json.loads(request.POST['data'])
        data['user'] = request.user.id
        score = ScoreForm(data).save()

        return JsonResponse({'status': 'OK'})

    else:
        return JsonResponse({'status': 'You Can Not Do This !'})
