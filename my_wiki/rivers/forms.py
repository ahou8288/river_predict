from django.forms import ModelForm
from .models import Section
from markdownx.fields import MarkdownxFormField

class SectionForm(ModelForm):

    class Meta:
        model = Section
        exclude = ['slug','creator','creation_time','recent_editor','last_edit_time',]
        myfield = MarkdownxFormField()
