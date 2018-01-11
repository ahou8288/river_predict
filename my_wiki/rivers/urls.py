from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('rivers', views.rivers, name='rivers'),
    path('levels', views.levels, name='levels'),
]