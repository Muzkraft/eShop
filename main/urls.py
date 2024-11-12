from django.views.decorators.cache import cache_page
from django.urls import path
from .views import IndexView, AboutView

app_name = 'main'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    # cache_page(60 * 5) - кеширование страницы "about" каждые 5 минут
    path("about", cache_page(60 * 5) (AboutView.as_view()), name="about"),
]
