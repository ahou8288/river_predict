from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('rivers', views.rivers, name='rivers'),
    path('sections/<slug:slug>/', views.sections, name='sections'),
    path('levels', views.levels, name='levels'),
    path('edit_section/<slug:slug>/',views.edit_section, name='edit_sections')
]