from django.contrib import admin

# Register your models here.
from .models import River, Section

admin.site.register(River)
admin.site.register(Section)