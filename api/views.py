from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import *
from users.models import UserProfile
from schedule.models import *
from submission.models import *
from core.settings.base import SUBMITTER_GROUP_ID

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.filter(user__is_active=True)
    #active_ids = UserProfile.objects.filter(user__is_active=True).value_list('pk')
    #queryset.exclude(user__group__in=[SUBMITTER_GROUP_ID] and user__submissions__isnull)
    serializer_class = UserProfileSerializer

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class StaffGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.filter(categories__in=[2])
    serializer_class = GroupSerializer

class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class TimeslotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Submission.objects.filter(status='A')
    serializer_class = SubmissionSerializer
