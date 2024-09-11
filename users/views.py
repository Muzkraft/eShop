from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from carts.models import Cart
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key # запоминаем ключ сессии еще не авторизованного пользователя
             
            user = form.instance 
            auth.login(request, user)
            
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user) # обновляем по ключу сессии корзину пользователя продуктами, которые он положил будучи не авторизованным
                    
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
            
            session_key = request.session.session_key # запоминаем ключ сессии еще не авторизованного пользователя
            
            if user:
                auth.login(request, user)
                messages.success(request, f'Добро пожаловать {username}, будьте как дома!')
                
                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user) # обновляем по ключу сессии корзину пользователя продуктами, которые он положил будучи не авторизованным
                
                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                
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


def users_cart(request):
    return render(request, 'users/users_cart.html')

@login_required()
def logout(request):
    messages.success(request, f'Ты это, {request.user.username}, заходи если что.')
    auth.logout(request)
    return redirect(reverse("main:index"))
