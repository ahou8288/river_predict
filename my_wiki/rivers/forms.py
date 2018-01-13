from django.forms import ModelForm
from .models import Section


class SectionForm(ModelForm):

    class Meta:
        model = Section
        fields = ['name', 'description', 'grade', 'river']
