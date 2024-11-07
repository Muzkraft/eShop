from pipes import Template
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, QuerySet
from django.db.models.base import Model as Model
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("user:profile")

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)
        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(
            self.request,
            f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт!",
        )
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Slastena - Регистрация"
        return context


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("main:index")

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        session_key = (
            self.request.session.session_key
        )  # запоминаем ключ сессии еще не авторизованного пользователя
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                # delete old authorized user carts
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                # add new authorized user carts from anonymous session
                Cart.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f"Добро пожаловать {user.first_name}!")
                return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse("user:logout"):
            return redirect_page
        return reverse_lazy("main:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Slastena - Авторизация"
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлён")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка!")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Slastena - личный кабинет"
        context["orders"] = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
            .order_by("-id")
        )
        return context


class UserCartView(TemplateView):
    template_name = "users/users_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Slastena - Корзина"
        return context


@login_required()
def logout(request):
    messages.success(request, f"Ты это, {request.user.username}, заходи если что.")
    auth.logout(request)
    return redirect(reverse("main:index"))


# @login_required()
# def profile(request):
#     if request.method == "POST":
#         form = ProfileForm(
#             data=request.POST, instance=request.user, files=request.FILES
#         )
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Ваш профиль успешно обновлён!")
#             return HttpResponseRedirect(reverse("user:profile"))
#     else:
#         form = ProfileForm(instance=request.user)

#     orders = (
#         Order.objects.filter(user=request.user)
#         .prefetch_related(
#             Prefetch(
#                 "orderitem_set",
#                 queryset=OrderItem.objects.select_related("product"),
#             )
#         )
#         .order_by("-id")
#     )

#     context = {"title": "Slastena - Личный кабинет", "form": form, "orders": orders}

#     return render(request, "users/profile.html", context)


# def users_cart(request):
#     return render(request, "users/users_cart.html")


# def registration(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()

#             session_key = (
#                 request.session.session_key
#             )  # запоминаем ключ сессии еще не авторизованного пользователя

#             user = form.instance
#             auth.login(request, user)

#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(
#                     user=user
#                 )  # обновляем по ключу сессии корзину пользователя продуктами, которые он положил будучи не авторизованным

#             messages.success(
#                 request, f"Мы рады знакомству {user.username}, проходите пожалуйста!"
#             )
#             return HttpResponseRedirect(reverse("main:index"))
#     else:
#         form = UserRegistrationForm()

#     context = {
#         "title": "Slastena - Регистрация",
#         "form": form,
#     }
#     return render(request, "users/registration.html", context)

# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = auth.authenticate(username=username, password=password)

#             session_key = (
#                 request.session.session_key
#             )  # запоминаем ключ сессии еще не авторизованного пользователя

#             if user:
#                 auth.login(request, user)
#                 messages.success(
#                     request, f"Добро пожаловать {username}, будьте как дома!"
#                 )

#                 if session_key:
#                     # delete old authorized user carts
#                     forgot_carts = Cart.objects.filter(user=user)
#                     if forgot_carts.exists():
#                         forgot_carts.delete()
#                     # add new authorized user carts from anonimous session
#                     Cart.objects.filter(session_key=session_key).update(
#                         user=user
#                     )  # обновляем по ключу сессии корзину пользователя продуктами, которые он положил будучи не авторизованным

#                 redirect_page = request.POST.get("next", None)
#                 if redirect_page and redirect_page != reverse("user:logout"):
#                     return HttpResponseRedirect(request.POST.get("next"))

#                 return HttpResponseRedirect(reverse("main:index"))
#     else:
#         form = UserLoginForm()

#     context = {
#         "title": "Slastena - Вход",
#         "form": form,
#     }
#     return render(request, "users/login.html", context)
