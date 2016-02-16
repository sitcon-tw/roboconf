from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import *
from users.models import UserProfile
from users.utils import sorted_groups
from schedule.models import *
from submission.models import *
from core.settings.base import SUBMITTER_GROUP_ID
from django.db.models import Q

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    _submissions = Submission.objects.filter(status__in=['A', 'Z'])
    _u_pks = [ s.user.pk for s in _submissions ]
    queryset = User.objects.filter(pk__in=_u_pks)
    serializer_class = UserSerializer

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.filter(user__is_active=True)
    #active_ids = UserProfile.objects.filter(user__is_active=True).value_list('pk')
    #queryset.exclude(user__group__in=[SUBMITTER_GROUP_ID] and user__submissions__isnull)
    serializer_class = UserProfileSerializer

class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class TimeslotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.order_by('timeslot__start', 'room__pk')
    serializer_class = ActivitySerializer

class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Submission.objects.filter(Q(status='A') | Q(status='Z'))
    serializer_class = SubmissionSerializer
