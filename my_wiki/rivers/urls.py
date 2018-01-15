from django.urls import path
from . import views
from rivers.views import SectionView, RiverView

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('rivers', views.rivers, name='rivers'),
    path('section/create', SectionView.as_view(), name='create section'),
    path('section/edit/<slug:slug>/', SectionView.as_view(), name='edit section'),
    path('section/view/<slug:slug>/', views.sections, name='view section'),
    path('river/create', RiverView.as_view(), name='create river'),
    path('levels', views.levels, name='levels'),
]