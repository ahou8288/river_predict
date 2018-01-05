from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'home.html')
    
def levels(request):
    rivers = [
        {'name': 'Nymboida', 'level': 1.3},
        {'name': 'Barrington', 'level': 2.0},
    ]
    return render(request, 'levels.html', {'rivers':rivers})
