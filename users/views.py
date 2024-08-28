from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from users.forms import UserLoginForm
from django.urls import reverse

def registration(request):
    context = {
        'title': 'Slastena - Регистрация',
    }
    return render(request, 'users/registration.html', context)

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
        
        context = {
            'title': 'Slastena - Вход',
            'form': form,
        }
    return render(request, 'users/login.html', context)

def profile(request):
    context = {
        'title': 'Slastena - Личный кабинет',
    }
    return render(request, 'users/profile.html', context)

def logout(request):
    ...
