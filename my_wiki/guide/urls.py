from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'levels', views.levels, name='levels'),
    url(r'map_list', views.map_list, name='map_list'),
    url(r'map_view/(.*)$', views.map_view, name='map_view'),
]