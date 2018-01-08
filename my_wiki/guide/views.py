from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'home.html')


def levels(request):
    rivers = [
        {'name': 'Nymboida', 'level': 1.3},
        {'name': 'Barrington', 'level': 2.0},
    ]
    return render(request, 'levels.html', {'rivers': rivers})

maps = [{
    'name': 'Gwydir River',
    'url': 'gwydir',
    'embed': 'https://www.google.com/maps/d/u/0/embed?mid=1wZIXpfFOVdZweF1In8VUwOP1LwFyg9Dp',
}]


def map_list(request):
    return render(request, 'map_list.html', {'maps': maps})

def map_home(request):
    return render(request, 'map_home.html')

def map_view(request, river_name):
    for i in maps:
        if river_name == i['url']:
            return render(request, 'map_view.html', {'url': i['embed'], 'name': river_name})
    print('Not found')
