from django.urls import include, path
from django.contrib import admin
from django.http import HttpResponseRedirect

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('rivers/')),
    path('rivers/', include('rivers.urls')),
    path('admin/', admin.site.urls),
]