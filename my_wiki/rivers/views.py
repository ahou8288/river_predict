from django.shortcuts import render
from .models import River, Section, Level, Gauge

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
    print('Checking if river data has been downloaded.')

    print('Getting data for all rivers.')
    all_rivers={
        '1234':{
            'discharge':[1,2],
            'levels':[11,21],
            'name':'Doggo Paradise River'
            }
        }
    return render(request, 'levels.html', {'PAGE_TITLE': 'Levels'})
