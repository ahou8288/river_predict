from django.forms import ModelForm, ModelChoiceField, FloatField
from .models import Section, Gauge, River, Point
from markdownx.fields import MarkdownxFormField


class SectionForm(ModelForm):

    class Meta:
        model = Section
        fields = ['name', 'river', 'grade', 'description', 'minimum']
        myfield = MarkdownxFormField()

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        self.fields['gauge'].required = False
        self.fields['minimum'].required = False


class RiverForm(ModelForm):

    class Meta:
        model = River
        fields = ['name', 'description', 'gauge']
