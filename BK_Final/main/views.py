from django.shortcuts import render, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

menu = [{'title': "О проекте", 'url_name': 'about'},
        {'title': "Посмотреть корзину", 'url_name': 'shoe_box'},
        {'title': "Посмотреть заказы", 'url_name': 'show_order'},
        {'title': "Регистрация ", 'url_name': 'register'},
        {'title': "Войти ", 'url_name': 'login'},
]

# menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

# @csrf_exempt
# def tests(request):
#
#     if request.method == "GET":
#         return render(request, 'main/main.html',context={"title" : 'Hello world GET'})
#     if request.method == "POST":
#         return HttpResponse('Hello world POST')


def about(request):
    return render(request, 'main/about.html')

def index(request):
    prod = Products.objects.all()
    context = {
        'prod' : prod,
        'menu' : menu,
        'title' : 'Главная страница',
        'sel_cat' : 0,
    }

    return render(request, 'main/index.html', context=context)

def show_cat(request, cat_id):
    prod = Products.objects.filter(cat_id=cat_id)

    if len(prod) == 0:
        raise Http404()

    context = {
        'prod': prod,
        'menu': menu,
        'title': 'Отображение по рубрикам',
        'sel_cat': cat_id,
    }

    return render(request, 'main/index.html', context=context)

def show_prod(request, prod_id):
    return HttpResponse(f'ображение подробной информации о товаре с ид = {prod_id}')

def add_box(request,prod_id):
    print(f'Добавление товара с ид {prod_id} в корзину ')
    # usr =
    prod = Products.objects.get(pk=prod_id)
    print(f'тегория выбранного товара {prod.cat_id}')
    context = {
        'prod': prod,
        'menu': menu,

    }
    return render(request, 'main/index.html', context=context)

def show_box(request):
    pass

def login(request):
    return HttpResponse('Autorisation')

def register(request):
    pass
