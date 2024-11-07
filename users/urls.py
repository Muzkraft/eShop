from django.urls import path
from users import views 

app_name = 'users'

urlpatterns = [
    path("registration/", views.UserRegistrationView.as_view(), name="registration"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("users-cart/", views.UserCartView.as_view(), name="users_cart"),
    path("logout/", views.logout, name="logout"),
]
