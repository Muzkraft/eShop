from django.urls import path
from users.views import login, registration, profile, logout, users_cart

app_name = 'users'

urlpatterns = [
    path("registration/", registration, name="registration"),
    path("login/", login, name="login"),
    path("profile/", profile, name="profile"),
    path("users-cart/", users_cart, name="users_cart"),
    path("logout/", logout, name="logout"),
]
