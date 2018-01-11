from django.contrib import admin

# Register your models here.
from .models import River, Section, Gauge, Level

admin.site.register(River)
admin.site.register(Section)
admin.site.register(Gauge)
admin.site.register(Level)