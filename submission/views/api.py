from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from submission.models import Submission
from core.settings.base import SUBMISSION_END
from core.api.views import render_json
from core.api.decorators import api_endpoint, ajax_required
import datetime

@api_endpoint(public=True)
def all(request):
	return render_json(request, {
		'status': 'success',
		'submissions': [
			{
				'speaker': s.user.profile.display_name,
				'speakerbio': s.user.profile.bio,
                'avatar': s.user.profile.avatar(),
				'title': s.title,
				'type': dict(Submission.SUBMISSION_TYPES)[s.type],
				'abstract': s.abstract,
                'room': s.room.fullname if s.room else None,
                'time': s.time.isoformat() if s.time else None,
			}
			for s in Submission.objects.filter(status='A').order_by('type', 'id')
		],
	})
