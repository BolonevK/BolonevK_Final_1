from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, Http404, HttpResponse, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from django.views.generic import CreateView, ListView, DetailView
from .forms import *
from .models import *


# user: root1, pass: testpass


menu = [{'title': "О проекте", 'url_name': 'about'},
        {'title': "Посмотреть корзину", 'url_name': 'show_box'},
        {'title': "Посмотреть заказы", 'url_name': 'show_order'},
        {'title': "Регистрация ", 'url_name': 'register'},
        {'title': "Выйти", 'url_name': 'logout_user'},
        {'title': "Войти ", 'url_name': 'login'},
        ]

def about(request):

    return render(request, 'main/about.html', context={'menu' : menu})


class MarketMain(ListView):
    model = Products
    template_name = 'main/index.html'
    context_object_name = 'prod'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['sel_cat'] = 0
        return context

class ShowCat(ListView):            # Отображение товара по категориям
    model = Products                # указание модель на основе которой будет строиться форма
    template_name = 'main/index.html'  # адрес страницы, для для создания формы
    context_object_name = 'prod'    # наименование переменной для HTML страницы
    allow_empty = False             # отработка ошибки, если ввели неправильную категорию

    def get_queryset(self):
        return Products.objects.filter(cat_id=self.kwargs['cat_id'])     # условие для отбора данных модели.
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Категория - '+ str(context['prod'][0].cat)
        context['sel_cat'] = context['prod'][0].cat_id,
        return context

class ShowProd(DetailView):
    model = Products  # указание модель на основе которой будет строиться форма
    template_name = 'main/show_prod.html'  # адрес страницы, для для создания формы
    pk_url_kwarg = 'prod_id'
    context_object_name = 'prod'  # наименование переменной для HTML страницы
    def get_context_data(self, *, object_list=None, **kwargs):
        fb = FeedBack.objects.filter(product=self.kwargs['prod_id'])
        sr = fb.aggregate(Avg('fb_mark'))
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Подробно о товаре'
        context['sel_cat'] = context['object'].cat_id
        context['fb'] = fb
        context['sr'] = sr['fb_mark__avg']
        return context

# class AddFeedback(CreateView):
#     form_class = AddFeedbackForm
#     template_name = 'main/feedback.html'
#


# def index(request):
#     prod = Products.objects.all()
#
#     context = {
#         'prod' : prod,
#         'menu' : menu,
#         'title' : 'Главная страница',
#         'sel_cat' : 0,}
#     if request.user.is_authenticated : context['menu'].append({'title' : 'Клиент: '+request.user.username, 'url_name': 'login'})
#     return render(request, 'main/index.html', context=context)

# def show_cat(request, cat_id):
#     prod = Products.objects.filter(cat_id=cat_id)
#     if len(prod) == 0:
#         raise Http404()
#     context = {
#         'prod': prod,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'sel_cat': cat_id,
#     }
#     return render(request, 'main/index.html', context=context)

# def show_prod(request, prod_id):
#     prod = Products.objects.get(pk=prod_id)
#
#     fb = FeedBack.objects.filter(product = prod_id)
#     sr = fb.aggregate(Avg('fb_mark'))
#     context = {
#         'prod': prod,
#         'fb' : fb,
#         'menu': menu,
#         'title': 'Подробно о товаре',
#         'sr' : sr['fb_mark__avg'],
#     }
#     return render(request, 'main/show_prod.html', context=context)

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
        print(form.data)
        fb = FeedBack(fb_text=form.data['fb_text'],
                      fb_mark=form.data['fb_mark'],
                      product=Products.objects.get(pk=prod_id),
                      user=User.objects.get(pk=2))
        fb.save()
        return redirect('prod', prod_id)
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


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    # clients_form = ClientsForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Регистрация")
    #     return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Авторизация")
    #     return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
