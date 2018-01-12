from django.contrib import admin

# Register your models here.
from .models import River, Section, Gauge, Level

admin.site.register(River)
admin.site.register(Gauge)
admin.site.register(Level)
from markdownx.admin import MarkdownxModelAdmin
admin.site.register(Section, MarkdownxModelAdmin)