from django.shortcuts import render

def registration(request):
    context = {
        'title': 'Slastena - Регистрация',
    }
    return render(request, 'users/registration.html', context)

def login(request):
    context = {
        'title': 'Slastena - Вход',
    }
    return render(request, 'users/login.html', context)

def profile(request):
    context = {
        'title': 'Slastena - Личный кабинет',
    }
    return render(request, 'users/profile.html', context)

def logout(request):
    ...
