from django.conf.urls import url, include
from api import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'staffgroups', views.StaffGroupViewSet)
router.register(r'userprofiles', views.UserProfileViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'timeslots', views.TimeslotViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'submissions', views.SubmissionViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls))
]
