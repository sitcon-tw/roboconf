from django.shortcuts import render
from core.api.views import render_json
from core.api.decorators import api_endpoint, ajax_required
from schedule.models import *
from core.settings.base import TIME_ZONE
import pytz

@api_endpoint(public=True)
def all(request):
	return render_json(request, {
		'status': 'success',
		'activities': [
			{
                'description': a.description,
                'room': a.room.fullname if a.room else None,
                'time': a.timeslot.start.astimezone(pytz.timezone(TIME_ZONE)).strftime('%X'),
                'submission': a.submission.pk if a.submission else None
			}
			for a in Activity.objects.order_by('timeslot__start')
		],
	})
