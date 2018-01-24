from django.contrib import admin

# Register your models here.
from .models import River, Section, Gauge, Level, Interested, Point

admin.site.register(River)
admin.site.register(Gauge)
admin.site.register(Level)
admin.site.register(Interested)
admin.site.register(Point)
from markdownx.admin import MarkdownxModelAdmin
admin.site.register(Section, MarkdownxModelAdmin)