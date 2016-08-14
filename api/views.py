from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from api.serializers import *
from users.models import UserProfile
from users.utils import sorted_users, sorted_groups, sorted_categories
from django.db.models import QuerySet
from oauth2_provider.ext.rest_framework import TokenHasScope

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def list(self, request):
        serializer = UserSerializer(sorted_users(self.queryset), many=True, context={ 'request': request } )
        return Response(serializer.data)

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.filter(user__is_active=True)
    #active_ids = UserProfile.objects.filter(user__is_active=True).value_list('pk')
    serializer_class = UserProfileSerializer

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def list(self, request):
        serializer = GroupSerializer(sorted_groups(self.queryset), many=True, context={ 'request': request } )
        return Response(serializer.data)

class StaffGroupViewSet(GroupViewSet):
    queryset = Group.objects.filter(categories__id=2)

class Me(generics.ListAPIView):
    serializer_class = UserPrivateSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['read_personal_data']

    def get_queryset(self):
            return [self.request.user] # FIXME should return a QuerySet but somehow this works
