from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthForm
from django.contrib.auth.models import User

urlpatterns = [

    # url(r'^$', views.HomePage.as_view(), name='home'),

    # Register new user
    url(r'^signup/', views.SignUp.as_view(), name='signup'),

    # Login URL
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html', 'authentication_form': CustomAuthForm}, name='login'),
    url(r'^$', auth_views.login, 
        {'template_name': 'home.html', 
        'authentication_form': CustomAuthForm, 
        'extra_context': 
            {'recommendations': views.recommendation_list } 
        }, name='home-login'),

    # Logout URL
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    # Reset password
    url(r'^password_reset/$', auth_views.password_reset, {'post_reset_redirect': '/password_reset/done/'}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm, {'post_reset_redirect': '/reset/done/'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,  name='password_reset_complete'),
    
    # Send an activation URL 
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),

    # Activation URL
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    # Profile URL's
    url(r'^profile/$', views.ViewProfile.as_view(), name='view_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.ViewProfile.as_view(), name='view_profile_with_pk'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/password/$', views.ChangePassword.as_view(), name='change_password'),

]
