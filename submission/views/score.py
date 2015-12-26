from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg, Count
from submission.models import Submission, Score
from submission.forms import ScoreForm
from core.settings.base import SUBMISSION_END
import json
import datetime

def get_score(submission_id, user_id):
    result = Score.objects.filter(submission_id=submission_id, user_id=user_id)

    if len(result) > 0:
        result = result[0]
    else:
        result = None

    return result

@login_required
def score(request):
    if request.user.has_perm('submission.review'):

        submissions = Submission.objects.order_by('type', 'id').exclude(user=request.user)
        total = submissions.count()
        scores = [ get_score(s.id, request.user.id) for s in submissions ]

        context = {
            'submissions_total': total,
            'submissions': zip(submissions, scores),
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

        try:
            instance = Score.objects.get(user_id=request.user.id, submission_id=data['submission'])
        except:
            instance = None

        if instance:
            score = ScoreForm(data, instance=instance).save()
        else:
            score = ScoreForm(data).save()

        return JsonResponse({'status': 'OK'})

    else:
        return JsonResponse({'status': 'You Can Not Do This !'})

@login_required
def score_total(request):
    if request.user.has_perm('submission.view_total_score'):
        submissions = Submission.objects.filter(
                                scores__audience__gt=0,
                                scores__cool__gt=0,
                                scores__expression__gt=0,
                                scores__difficulty__gt=0,
                            ).annotate(
                                scores_number=Count('scores__audience'),
                                audience=Avg('scores__audience'),
                                cool=Avg('scores__cool'),
                                expression=Avg('scores__expression'),
                                difficulty=Avg('scores__difficulty'),
                            )

        for i in submissions:
            i.total_score = i.audience + i.cool + i.expression

        submissions.order_by('-total_score')

        context = {
            'submissions': submissions,
            'user': request.user,
        }

        return render(request, 'submission/score_total.html', context)

    else:
        return redirect('submission:list')
