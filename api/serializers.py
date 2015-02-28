from django.contrib.auth.models import User, Group
from rest_framework import serializers
from users.models import UserProfile
from users.utils import sorted_users
from schedule.models import *
from submission.models import *

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'user', 'display_name', 'bio', 'title', 'avatar')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('url', 'profile', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('url', 'name', 'users')

    def get_users(self, group):
        users = sorted_users(User.objects.filter(groups=group).filter(is_active=True))
        serializer = UserSerializer(instance=users, many=True, context={'request': self.context['request']})
        return serializer.data

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('url', 'shortname', 'fullname', 'activity_set')

class TimeslotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Timeslot
        fields = ('url', 'start', 'end', 'activity_set')

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    start = serializers.DateTimeField(source='timeslot.start')
    end = serializers.DateTimeField(source='timeslot.end')
    room = serializers.CharField(source='room.fullname')
    title = serializers.CharField(source='submission.title')
    abstract = serializers.CharField(source='submission.abstract')
    speaker = serializers.CharField(source='submission.user.profile.display_name')

    class Meta:
        model = Activity
        fields = ('url', 'description', 'start', 'end', 'room', 'title', 'abstract', 'speaker', 'submission')

class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    speaker = serializers.CharField(source='user.profile.display_name')
    bio = serializers.CharField(source='user.profile.bio')
    avatar = serializers.CharField(source='user.profile.avatar')
    start = serializers.DateTimeField(source='activity.timeslot.start')
    end = serializers.DateTimeField(source='activity.timeslot.end')
    room = serializers.CharField(source='activity.room.fullname')

    class Meta:
        model = Submission
        fields = ('url', 'speaker', 'bio', 'avatar', 'title', 'type', 'abstract', 'start', 'end', 'room', 'activity')
