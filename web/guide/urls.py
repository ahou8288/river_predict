from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('levels', views.levels, name='levels'),
]