from django.contrib.auth.models import User, Group
from rest_framework import serializers
from users.models import UserProfile

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'profile', 'username', 'groups')

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'display_name', 'bio', 'title', 'avatar')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
