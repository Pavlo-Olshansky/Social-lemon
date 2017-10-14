from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.authtoken import views as auth_view

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', views.UserListRetrieveViewSet, base_name='users')

urlpatterns = (
    url(r'^$', views.api_docs, name="api_docs"),
	url(r'^', include(router.urls)),

    # url(r'^users/$', views.UserList.as_view(), name="list_view"),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetailsView.as_view(), name="detail_view"),

    url(r'^api-token-auth/', views.ObtainAuthToken.as_view(), name='api_token_auth'),
    

)

# urlpatterns = format_suffix_patterns(urlpatterns)

