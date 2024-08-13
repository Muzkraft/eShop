
from django.shortcuts import render

from goods.models import Categories


def index(request):
    
    
    context = {
        'title': 'Home - Главная',
        'content': 'Кондитерский цех Slastena.ru',
    }
    return render(request, 'main/index.html', context)

def about(request):
    context = {'title': 'Home - О нас',
               'content': 'Кондитерский цех Slastena.ru',
               'text_on_page': 'Some text'
               }
    return render(request, 'main/about.html', context)