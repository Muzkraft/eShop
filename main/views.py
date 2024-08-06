from http.client import HTTPResponse
from turtle import title
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {'title': 'Home - Главная',
               'content': 'Кондитерский цех Slastena.ru',
               }
    return render(request, 'main/index.html', context)

def about(request):
    context = {'title': 'Home - О нас',
               'content': 'Кондитерский цех Slastena.ru',
               }
    return render(request, 'main/about.html', context)