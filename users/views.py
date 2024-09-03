from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f'Мы рады знакомству {user.username}, проходите пожалуйста!')
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserRegistrationForm()

    context = {
        "title": "Slastena - Регистрация",
        "form": form,
    }
    return render(request, "users/registration.html", context)


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f'Добро пожаловать {username}, будьте как дома!')
                return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserLoginForm()

    context = {
        "title": "Slastena - Вход",
        "form": form,
    }
    return render(request, "users/login.html", context)


@login_required()
def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            data=request.POST, instance=request.user, files=request.FILES
        )
        if form.is_valid():
            form.save()
            messages.success(request, f'Ваш профиль успешно обновлён!')
            return HttpResponseRedirect(reverse("user:profile"))
    else:
        form = ProfileForm(instance=request.user)

    context = {
        "title": "Slastena - Личный кабинет",
        "form": form,
    }

    return render(request, "users/profile.html", context)


@login_required()
def logout(request):
    messages.success(request, f'Ты это, {request.user.username}, заходи если что.')
    auth.logout(request)
    return redirect(reverse("main:index"))
