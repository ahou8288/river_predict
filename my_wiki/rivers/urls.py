from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('rivers', views.rivers, name='rivers'),
    path('section/edit/<slug:slug>/',views.edit_section, name='edit section'),
    path('section/view/<slug:slug>/', views.sections, name='view section'),
    path('levels', views.levels, name='levels'),
]