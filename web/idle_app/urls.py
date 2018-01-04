from django.conf.urls import url

from . import views
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'landing', views.landing, name='landing'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^.*', views.bad_url, name='bad_url'),
]
