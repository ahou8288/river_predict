from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'home.html')

def rivers(request):
    return render(request, 'rivers.html')

def levels(request):
    return render(request, 'levels.html')