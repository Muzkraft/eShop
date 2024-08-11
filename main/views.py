from http.client import HTTPResponse
from turtle import title
from django.shortcuts import render
from django.http import HttpResponse
from goods.models import Categories


def index(request):
    categories = Categories.objects.all()
    
    context = {'title': 'Home - Главная',
               'content': 'Кондитерский цех Slastena.ru',
               'categories': categories,
               }
    return render(request, 'main/index.html', context)

def about(request):
    context = {'title': 'Home - О нас',
               'content': 'Кондитерский цех Slastena.ru',
               'text_on_page': 'Some text'
               }
    return render(request, 'main/about.html', context)