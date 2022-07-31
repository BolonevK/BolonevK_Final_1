from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, Http404, HttpResponse, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from django.views.generic import CreateView
from .forms import *
from .models import *

menu = [{'title': "О проекте", 'url_name': 'about'},
        {'title': "Посмотреть корзину", 'url_name': 'show_box'},
        {'title': "Посмотреть заказы", 'url_name': 'show_order'},
        {'title': "Регистрация ", 'url_name': 'register'},
        {'title': "Войти ", 'url_name': 'login'},
]


def about(request):

    return render(request, 'main/about.html', context={'menu' : menu})

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
    prod = Products.objects.get(pk=prod_id)
    fb = FeedBack.objects.filter(product = prod_id)
    sr = fb.aggregate(Avg('fb_mark'))
    # sr = FeedBack.objects.filter().aggregate(Avg('fb_mark'))
    context = {
        'prod': prod,
        'fb' : fb,
        'menu': menu,
        'title': 'Подробно о товаре',
        'sr' : sr['fb_mark__avg'],
    }
    return render(request, 'main/show_prod.html', context=context)

def add_box(request,prod_id):
    prod = Products.objects.get(pk=prod_id)
    print(f'тегория выбранного товара {prod.cat_id}')
    context = {
        'prod': prod,
        'menu': menu,
    }
    # return render(request, 'main/index.html', context=context)
    return redirect('prod', prod_id)

def add_feedback(request,prod_id):
    if request.method == 'POST':
        form = AddFeedbackForm(request.POST)
    else:
        form = AddFeedbackForm()

    prod = Products.objects.get(pk=prod_id)
    context = {
        'prod': prod,
        'menu': menu,
        'title': 'Добавление отзыва о товаре',
        'form' : form,
        'prod_id': prod_id
    }
    return render(request,'main/feedback.html',context=context)

def show_box(request):
    pass

def show_order(request):
    pass

def login(request):
    return HttpResponse('Autorisation')

# class RegisterUser(CreateView):
#     form_class = UserCreationForm
#     template_name = 'main/register.html'
#     success_url = reverse_lazy('login')

