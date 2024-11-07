
from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Categories


# def index(request):
    
    
#     context = {
#         'title': 'Home - Главная',
#         'content': 'Кондитерский цех Slastena.ru',
#     }
#     return render(request, 'main/index.html', context)

class IndexView(TemplateView):
    template_name = 'main/index.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Главная'
        context['content'] = 'Кондитерский цех Slastena.ru'

        return context

# def about(request):
#     context = {'title': 'Home - О нас',
#                'content': 'Кондитерский цех Slastena.ru',
#                'text_on_page': 'Some text'
#                }
#     return render(request, 'main/about.html', context)

class AboutView(TemplateView):
    template_name = 'main/about.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - О нас'
        context['content'] = 'О нас'
        context['text_on_page'] = '...'
        return context