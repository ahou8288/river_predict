from django.contrib import admin

# Register your models here.
from .models import River, Section, Gauge, Level, Interested, Point

# Extra addons
from reversion.admin import VersionAdmin

admin.site.register(Gauge)
admin.site.register(Level)
admin.site.register(Interested)

@admin.register(Point)
class PointAdmin(VersionAdmin):
    pass

@admin.register(Section)
class SectionAdmin(VersionAdmin):
    pass

@admin.register(River)
class RiverAdmin(VersionAdmin):
    pass

