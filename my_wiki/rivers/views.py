from django.shortcuts import render
from .models import River, Section, Level, Gauge
from django.utils import timezone
import datetime
import math
import sys
sys.path.insert(0, './rivers/lib')
import gauge_download

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
    download_data = gauge_download.download_or_get_rivers().items()
    for download_id, data in download_data:
        print(data)
        if data['name']:

            if Gauge.objects.filter(name=data['name']).count():
                print('Adding new gauge {}'.format(data['name']))
                g = Gauge.objects.get(name=data['name'])
            else:
                print('Adding new gauge {}'.format(data['name']))
                g = Gauge(name=data['name'], download_id=download_id)
                g.save()

            if not math.isnan(data['discharge']):
                print('Discharge reading added for {}'.format(data['name']))
                l1 = Level(unit='discharge', gauge=g, value=data['discharge'])
                l1.save()
            else:
                print('nan found discharge')
            if not math.isnan(data['levels']):
                print('Level reading added for {}'.format(data['name']))
                l2 = Level(unit='level', gauge=g, value=data['levels'])
                l2.save()
            else:
                print('nan found level')

    return render(request, 'levels.html', {'PAGE_TITLE': 'Levels'})
