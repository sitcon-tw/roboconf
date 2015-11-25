from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, permissions
from api.serializers import *
from users.models import UserProfile
from users.utils import sorted_groups
from django.db.models import QuerySet
from oauth2_provider.ext.rest_framework import TokenHasScope

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.filter(user__is_active=True)
    #active_ids = UserProfile.objects.filter(user__is_active=True).value_list('pk')
    serializer_class = UserProfileSerializer

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return sorted_groups(Group.objects.all())

class StaffGroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return sorted_groups(Group.objects.filter(categories__id=2))

class Me(generics.ListAPIView):
    serializer_class = UserPrivateSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['read_personal_data']

    def get_queryset(self):
            return [self.request.user] # FIXME should return a QuerySet but somehow this works
