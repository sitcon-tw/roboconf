from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import *
from users.models import UserProfile
from users.utils import sorted_groups
from schedule.models import *
from submission.models import *
from django.db.models import Q

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.filter(user__is_active=True)
    serializer_class = UserProfileSerializer

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return sorted_groups(Group.objects.all())

class StaffGroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return sorted_groups(Group.objects.filter(categories__id=2))

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
