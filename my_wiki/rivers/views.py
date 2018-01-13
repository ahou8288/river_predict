from django.shortcuts import render
from .models import River, Section, Level, Gauge
from django.db.models import Max
from rivers import forms
import sys
sys.path.insert(0, './rivers/lib')
import gauge_download  # this actually runs it lol

# Create your views here.


def index(request):
    return render(request, 'home.html', {'PAGE_TITLE': 'Homepage'})


def rivers(request):
    output = []
    rivers = River.objects.all()
    for river in rivers:
        sections = Section.objects.filter(river=river)
        output.append({
            'name': river.name,
            'sections': sections
        })
    return render(request, 'rivers.html', {'rivers': output, 'PAGE_TITLE': 'Rivers'})


def levels(request):
    gauges = Gauge.objects.all()
    data = []
    for gauge in gauges:
        latest_time = Level.objects.filter(
            gauge=gauge).aggregate(time=Max('time'))['time']
        try:
            level = Level.objects.get(gauge=gauge, time=latest_time)
            data.append({
                'name': gauge.name,
                'type': level.unit,
                'value': level.value,
                'time': level.time
            })
        except:
            pass
    return render(request, 'levels.html', {'PAGE_TITLE': 'Levels', 'data': data})


def sections(request, slug):
    section = Section.objects.get(slug=slug)
    river = section.river

    return render(request, 'section.html', {'PAGE_TITLE': section.name, 'section': section, 'river': river})


def edit_section(request, slug):
    section = Section.objects.get(slug=slug)
    form = forms.SectionForm(instance=section)
    return render(request, 'form.html', {'PAGE_TITLE': 'Editing ' + section.name, 'form': form})
