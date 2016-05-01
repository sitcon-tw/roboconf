from django.conf.urls import url, include
from api import views
from rest_framework import routers, reverse, response
from rest_framework import views as framework_views

# copied from https://stackoverflow.com/a/23321478/446391
class HybridRouter(routers.DefaultRouter):
    def __init__(self, *args, **kwargs):
        super(HybridRouter, self).__init__(*args, **kwargs)
        self._api_view_urls = {}
    def add_api_view(self, name, url):
        self._api_view_urls[name] = url
    def remove_api_view(self, name):
        del self._api_view_urls[name]
    @property
    def api_view_urls(self):
        ret = {}
        ret.update(self._api_view_urls)
        return ret

    def get_urls(self):
        urls = super(HybridRouter, self).get_urls()
        for api_view_key in self._api_view_urls.keys():
            urls.append(self._api_view_urls[api_view_key])
        return urls

    def get_api_root_view(self):
        # Copy the following block from Default Router
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, framework_viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)
        api_view_urls = self._api_view_urls

        class APIRoot(framework_views.APIView):
            _ignore_model_permissions = True

            def get(self, request, format=None):
                ret = {}
                for key, url_name in api_root_dict.items():
                    ret[key] = reverse.reverse(url_name, request=request, format=format)
                # In addition to what had been added, now add the APIView urls
                for api_view_key in api_view_urls.keys():
                    ret[api_view_key] = reverse.reverse(api_view_urls[api_view_key].name, request=request, format=format)
                return response.Response(ret)

        return APIRoot.as_view()

# Create a router and register our viewsets with it.
router = HybridRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet, base_name='group')
router.register(r'staffgroups', views.StaffGroupViewSet, base_name='staffgroup')
router.register(r'userprofiles', views.UserProfileViewSet)
router.add_api_view('me', url(r'^me$', views.Me.as_view(), name='me'))

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
