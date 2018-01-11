from django.shortcuts import render
from .models import River, Section

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
    return render(request, 'levels.html', {'PAGE_TITLE': 'Levels'})
