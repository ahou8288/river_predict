from django.contrib.auth.forms import AuthenticationForm, authenticate
from django.contrib.auth import logout, authenticate, login, get_user
from idle_app.forms import RegistrationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
import json
import datetime


# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
# from django.shortcuts import render, redirect

def landing(request):
    """
    api.create_game(request) Returns a UserGame
    object for implementing the create game button
    """

    if request.user.is_authenticated:
        # print(api.create_game(request))
        if request.method == 'GET':
            last_game = None
            try:
                last_game = UserGame.objects.filter(user=get_user(request)).reverse()[0].game
            except Exception:
                pass
            return render(request, 'landing.html', {
                "default_linking_code": "Enter Linking Code!"})
    else:
        return HttpResponseRedirect('/idle_app/login')


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/idle_app/landing/')

    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, '_login.html', {'form': form})

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user, request)
                login(request, user)
                return HttpResponseRedirect('/idle_app/landing/')
            else:
                print('User not found')
                return render(request, '_login.html', {'form': form})
        else:
            # If there were errors, we render the form with these
            # errors
            return render(request, '_login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, '_logout.html')

def bad_url(request):
    logout(request)
    return render(request, 'bad_url.html')

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return HttpResponseRedirect('/idle_app/landing/')
    else:
        form = RegistrationForm()
    return render(request, 'sign_up.html', {'form': form})
