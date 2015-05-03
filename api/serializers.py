from django.contrib.auth.models import User, Group
from rest_framework import serializers
from users.models import UserProfile
from users.utils import sorted_users

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
