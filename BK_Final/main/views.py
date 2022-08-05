from django.contrib.auth import logout, login
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
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin


# user: root,  pass: testpassword
# user: root1, pass: testpass
# user: vasay, pass: 1qazcde3
# user: user1, pass: userpass
# user: user2, pass: petrpass


menu = [{'title': "О проекте", 'url_name': 'about'},
        {'title': "Заказы", 'url_name': 'order_list'},
        {'title': "Выйти", 'url_name': 'logout_user'},
        ]

def about(request):
    return render(request, 'main/about.html', context={'menu' : menu})



class MarketMain(DataMixin,ListView):
    model = Products
    template_name = 'main/index.html'
    context_object_name = 'prod'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))


class ShowBox(DataMixin,ListView):
    model = OrderItems
    template_name = 'main/show_box.html'  # адрес страницы, для для создания формы
    context_object_name = 'order'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Информация по заказу')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        try:
            user_box = Orders.objects.get(user_id=self.request.user.pk, id=self.kwargs['order_id'])
        except:
            if self.request.user.is_staff:
                try:
                    user_box = Orders.objects.get(id=self.kwargs['order_id'])
                except:
                    raise Http404()
        return OrderItems.objects.filter(order_id=user_box.pk, i_count__gt=0)


class ShowCat(DataMixin,ListView):            # Отображение товара по категориям
    model = Products                # указание модель на основе которой будет строиться форма
    template_name = 'main/index.html'  # адрес страницы, для для создания формы
    context_object_name = 'prod'    # наименование переменной для HTML страницы
    allow_empty = False             # отработка ошибки, если ввели неправильную категорию

    def get_queryset(self):
        return Products.objects.filter(cat_id=self.kwargs['cat_id'])     # условие для отбора данных модели.

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - '+ str(context['prod'][0].cat),
                                      sel_cat = context['prod'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

class OrderList(DataMixin,ListView):
    model = Orders
    template_name = 'main/order_list.html'
    context_object_name = 'order'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            client = Clients.objects.get(user_id=self.request.user.pk)
            c_def = self.get_user_context(title='Заказы', client=client)
            return dict(list(context.items()) + list(c_def.items()))
        except:
            return context
    def get_queryset(self):
        try:
            ord = Orders.objects.filter(user_id=self.request.user.pk)
        except:
            raise Http404()
        return ord

class ShowProd(DataMixin,DetailView):
    model = Products  # указание модель на основе которой будет строиться форма
    template_name = 'main/show_prod.html'  # адрес страницы, для для создания формы
    pk_url_kwarg = 'prod_id'
    context_object_name = 'prod'  # наименование переменной для HTML страницы

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        fb = FeedBack.objects.filter(product=self.kwargs['prod_id'])
        sr = fb.aggregate(Avg('fb_mark'))
        c_def = self.get_user_context(title='Подробно о товаре', sel_cat=context['object'].cat_id,
                                      fb=fb, sr=sr['fb_mark__avg'])
        return dict(list(context.items()) + list(c_def.items()))



def add_box(request,prod_id):
    if request.user.is_authenticated:
        prod = Products.objects.get(pk=prod_id)
        try:# Проверка на существование товара в корзине клиента
            user_box = Orders.objects.get(user_id=request.user.pk, box= True)
            user_box.coast += prod.coast
        except:
            user_box = Orders(user= request.user, coast= prod.coast)
        user_box.save()
        try:
            oitem = OrderItems.objects.get(order_id=user_box.pk, item_id=prod.pk)
            oitem.i_count += 1
        except:
            oitem = OrderItems(order_id=user_box.pk, item_id=prod.pk, i_count=1)
        oitem.save()
        return redirect('prod', prod_id)
    else:
        return redirect('login')

def del_box(request,prod_id):
    prod = Products.objects.get(pk=prod_id)
    user_box = Orders.objects.get(user_id=request.user.pk, box=True)
    user_box.coast -= prod.coast
    user_box.save()
    oitem = OrderItems.objects.get(order_id=user_box.pk, item_id=prod.pk)
    oitem.i_count -= 1
    oitem.save()
    if OrderItems.objects.filter(order_id=user_box.pk, i_count__gt=0).exists():
        return redirect('show_box', user_box.pk)
    else:
        return redirect('order_list')

def add_feedback(request,prod_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddFeedbackForm(request.POST)
            fb = FeedBack(fb_text=form.data['fb_text'],
                          fb_mark=form.data['fb_mark'],
                          product=Products.objects.get(pk=prod_id),
                          user=User.objects.get(pk=request.user.id))
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
    else:
        return redirect('login')
def det_user(request,user_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DetailsUserForm(request.POST)
            if Clients.objects.filter(user_id=user_id).exists():
                usr = Clients.objects.get(user_id=user_id)
            else:
                usr = Clients()
                usr.user_id=user_id
            usr.address=form.data['address']
            usr.phone=form.data['phone']
            usr.save()
            return redirect('order_list')
        else:
            form = DetailsUserForm()
            form.data['phone'] = '+7'
        context = {
            'menu': menu,
            'title': 'Дополнительная информация',
            'form' : form,
        }
        return render(request,'main/det_user.html',context=context)
    else:
        return redirect('login')

def make_order(request,order_id):
    oitems = OrderItems.objects.filter(order_id=order_id)
    for oi in oitems:
        pr = Products.objects.get(pk=oi.item_id)
        pr.balance -= oi.i_count
        pr.save()
    order = Orders.objects.get(pk=order_id)
    order.box = False
    order.save()
    return redirect('show_box',order_id)

def pay_order(request,order_id):
    order = Orders.objects.get(pk=order_id)
    order.pay_it = True
    order.save()
    return redirect('show_box',order_id)


class RegisterUser(DataMixin,CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('det_user',user.pk)


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
