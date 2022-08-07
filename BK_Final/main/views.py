from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.forms import model_to_dict
from django.shortcuts import render, Http404, HttpResponse, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from django.views.generic import CreateView, ListView, DetailView
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import *
from .models import *
from .permissions import IsAdminOrReadOnly
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, viewsets
from .serializers import *

# user: root,  pass: testpassword
# user: root1, pass: testpass
# user: vasay, pass: 1qazcde3
# user: user1, pass: userpass
# user: user2, pass: petrpass


menu = [{'title': "О проекте", 'url_name': 'about'},    # Пункты меню по умолчанию (для функций)
        {'title': "Заказы", 'url_name': 'order_list'},
        {'title': "Выйти", 'url_name': 'logout_user'},
        ]



# страница "О проекте"
def about(request):
    return render(request, 'main/about.html', context={'menu' : menu})

# Вызов админ панели
def admin_panel(request):
    return render(request, '/admin/')

# Гланая страница проекта
class MarketMain(DataMixin,ListView):
    model = Products                        # строится на отображении объектов модели Products
    template_name = 'main/index.html'       # указывает на вызываемую страницу
    context_object_name = 'prod'            # переменная передаваемая в контекст переменных

    def get_context_data(self, *, object_list=None, **kwargs):  # функция получения и обогащения контекста данных
        context = super().get_context_data(**kwargs)            # получаем уже имеющийся контекст
        c_def = self.get_user_context(title='Главная страница') # формируем дополнение к контексту
        return dict(list(context.items()) + list(c_def.items()))    # передаем обьединенный контекст переменных на страницу

# класс отображения "Корзины" и заказа
class ShowBox(DataMixin,ListView):
    model = OrderItems                      # модель на основе котоой строится форма
    template_name = 'main/show_box.html'    # адрес страницы, для для создания формы
    context_object_name = 'order'           # переменная передаваемая в контекст переменных

    def get_context_data(self, *, object_list=None, **kwargs):      # функция получения и обогащения контекста данных
        context = super().get_context_data(**kwargs)                # получаем уже имеющийся контекст
        c_def = self.get_user_context(title='Информация по заказу') # формируем дополнение к контексту
        return dict(list(context.items()) + list(c_def.items()))    # передаем обьединенный контекст переменных на страницу

    def get_queryset(self):                 # функция по отбору данных для формы
        try:                                # пробуем получить номер заказа по пользователю и номеру заказа, что ы избежать возможность просматривать заказы других пользователей
            user_box = Orders.objects.get(user_id=self.request.user.pk, id=self.kwargs['order_id'])
        except:                             # если не получилось найти заказ
            if self.request.user.is_staff:  # проверяем имеет ли пользователь флаг is_staff
                try:                        # пробуем получить обьект заказа как администратор
                    user_box = Orders.objects.get(id=self.kwargs['order_id'])
                except:
                    raise Http404()         # если не получилось получить обьект заказа выдаем страницу с ошибкой 404
        return OrderItems.objects.filter(order_id=user_box.pk, i_count__gt=0)   # получаем товары, которые находятся в корзине и количество которых больше 0

# Отображение товара по категориям
class ShowCat(DataMixin,ListView):
    model = Products                # указание модель на основе которой будет строиться форма
    template_name = 'main/index.html'  # адрес страницы, для для создания формы
    context_object_name = 'prod'    # наименование переменной для HTML страницы
    allow_empty = False             # отработка ошибки, если ввели неправильную категорию

    def get_queryset(self):
        return Products.objects.filter(cat_id=self.kwargs['cat_id'])     # условие для отбора данных модели.

    def get_context_data(self, *, object_list=None, **kwargs):  # функция получения и обогащения контекста данных
        context = super().get_context_data(**kwargs)            # получаем уже имеющийся контекст
        c_def = self.get_user_context(title='Категория - '+ str(context['prod'][0].cat),    # формируем дополнение к контексту
                                      sel_cat = context['prod'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))         # передаем обьединенный контекст переменных на страницу

# отображение данных о пользователе и списка его заказов
class OrderList(DataMixin,ListView):
    model = Orders                          # указание модель на основе которой будет строиться форма
    template_name = 'main/order_list.html'  # адрес страницы, для для создания формы
    context_object_name = 'order'           # наименование переменной для HTML страницы

    def get_context_data(self, *, object_list=None, **kwargs):  # функция получения и обогащения контекста данных
        context = super().get_context_data(**kwargs)             # получаем уже имеющийся контекст
        try:             # пробуем получить дополнительные данные о пользователе (адрес, телефон)
            client = Clients.objects.get(user_id=self.request.user.pk)      # это не обязательные данные, пользователь мог не ввести их при регистрации
            c_def = self.get_user_context(title='Заказы', client=client)    # формируем дополнение к контексту
            return dict(list(context.items()) + list(c_def.items()))        # передаем обьединенный контекст переменных на страницу
        except:
            return context      # если доп. данные о пользователе получиь не удалось, возвращаем контекст как есть

    def get_queryset(self):     # условие для отбора данных модели.
        try:                    # пробуем выбрать все заказы пользователя по user.pk
            ord = Orders.objects.filter(user_id=self.request.user.pk)
        except:                 # если выбрать не удалось, например польщователь вручную ввел адрес с неправильным заказом
            raise Http404()     # возвращаем страницу 404
        return ord              # если все хорошо возвращаем queryset с заказами

# отображение подробной информации о товаре
class ShowProd(DataMixin,DetailView):
    model = Products                        # указание модель на основе которой будет строиться форма
    template_name = 'main/show_prod.html'   # адрес страницы, для для создания формы
    pk_url_kwarg = 'prod_id'                # переменная, которая передается из url
    context_object_name = 'prod'            # наименование переменной для HTML страницы

    def get_context_data(self, *, object_list=None, **kwargs):  # функция получения и обогащения контекста данных
        context = super().get_context_data(**kwargs)            # получаем уже имеющийся контекст
        fb = FeedBack.objects.filter(product=self.kwargs['prod_id'])    # получаем queryset с отзывами по определенному товару
        sr = fb.aggregate(Avg('fb_mark'))                       # получаем среднюю оценку по отзывам
        c_def = self.get_user_context(title='Подробно о товаре',  # формируем дополнение к контексту
                                      sel_cat=context['object'].cat_id,
                                      fb=fb, sr=sr['fb_mark__avg'])
        return dict(list(context.items()) + list(c_def.items()))    # передаем обьединенный контекст переменных на страницу

# функция по добавлению товара в "корзину" пользователя
def add_box(request,prod_id):
    if request.user.is_authenticated:       # проверяем пользователя на авторизацию
        prod = Products.objects.get(pk=prod_id)     # получаем объект товара
        try:                                        # Проверка на наличия уже открытого заказа у клиента
            user_box = Orders.objects.get(user_id=request.user.pk, box= True)
            user_box.coast += prod.coast            # если заказ есть, то увеличиваем сумму заказа
        except:                                     # если открытого заказа нет, то создаем новый
            user_box = Orders(user= request.user, coast= prod.coast)
        user_box.save()                             # сохраняем заказ
        try:                                        # Проверка на существование данного товара в корзине клиента
            oitem = OrderItems.objects.get(order_id=user_box.pk, item_id=prod.pk)
            oitem.i_count += 1                      # Если такой товар уже есть в "корзине", то увеличиваем его количество
        except:                                     # Если товар новый , то добавляем его в "корзину"
            oitem = OrderItems(order_id=user_box.pk, item_id=prod.pk, i_count=1)
        oitem.save()                                 # сохраняем запись о товаре
        return redirect('prod', prod_id)             # переход на страницу описания товара
    else:
        return redirect('login')     # усли польщователь не авторизован, переходим на страницу авторизации

# удаление товара из корзины
def del_box(request,prod_id):
    prod = Products.objects.get(pk=prod_id)       # получаем объект товара
    user_box = Orders.objects.get(user_id=request.user.pk, box=True)     # получаем объект заказа
    user_box.coast -= prod.coast                  # уменьшаем сумму заказа на стоимость удаляемого товара
    user_box.save()                               # сохраняем заказ
    oitem = OrderItems.objects.get(order_id=user_box.pk, item_id=prod.pk) # получаем строку копонента заказа (т.е. товара который находится в заказе пользователя)
    oitem.i_count -= 1                            # уменьшаем его количество на 1
    oitem.save()                                  # сохраняем компонент заказа
    if OrderItems.objects.filter(order_id=user_box.pk, i_count__gt=0).exists():  # если количество товара в заказе осталось > 0
        return redirect('show_box', user_box.pk)        # то просто обновляем страницу
    else:
        return redirect('order_list')               # если товара в заказе не осталось, то переходим на страницу пользователя

# добавление отзыва
def add_feedback(request,prod_id):
    if request.user.is_authenticated:                # проверка пользователя на аутентификацию
        if request.method == 'POST':                 # проверка метода
            form = AddFeedbackForm(request.POST)         # создаем объект формы и берем данные с формы
            fb = FeedBack(fb_text=form.data['fb_text'],      # создаем объект отзыва, по данным с формы
                          fb_mark=form.data['fb_mark'],
                          product=Products.objects.get(pk=prod_id),
                          user=User.objects.get(pk=request.user.id))
            fb.save()                                   # созраняем отзыв
            return redirect('prod', prod_id)            # переходим на страницу отображающую подробную информацию о товаре
        else:                                           # если метод GET
            form = AddFeedbackForm()                    # создаем объект формы
        prod = Products.objects.get(pk=prod_id)         # получаем объект продукта
        context = {                                     # создаем контекст переменных
            'prod': prod,
            'menu': menu,
            'title': 'Добавление отзыва о товаре',
            'form' : form,
            'prod_id': prod_id
        }
        return render(request,'main/feedback.html',context=context) # переходим на страницу отзывов и передаем ей контекст
    else:                                               # если пользователь не авторизован
        return redirect('login')                        # переходим на страницу авторизации

# заполнение дополнительных данных о пользователе (адрес, телефон)
def det_user(request,user_id):
    if request.user.is_authenticated:                   # проверка польщователя на аутентификацию
        if request.method == 'POST':                    # проверка метода зароса
            form = DetailsUserForm(request.POST)        # создаем объект формы с данными полученых в POST запросе
            if Clients.objects.filter(user_id=user_id).exists():    # если доп данные о пользователе уже существуют
                usr = Clients.objects.get(user_id=user_id)          # то получаем эти данные
            else:                                       # если доп данные о клиенте отсутствуют
                usr = Clients()                         # создаем объект данных
                usr.user_id=user_id                     # связываем данные с ид польщователя
                usr.save()                              # сохраняем созданый объект

            usr.address=form.data['address']            # устанавливаем данные адреса
            usr.phone=form.data['phone']                # устанавливаем данные телефона
            usr.save()                                  # сохраняем объект
            return redirect('order_list')               # переход на страницу отображения заказов, на которой так же отображаются данные пользователя
        else:                                           # если метод GET
            form = DetailsUserForm()                    # создаем объект формы
            # form.data['phone'] = '+7'
        context = {                                     # создаем контекст переменных
            'menu': menu,
            'title': 'Дополнительная информация',
            'form' : form,
        }                                               # переходим на страницу доп данных пользователя
        return render(request,'main/det_user.html',context=context)
    else:                                               # если польщователь не авторизирован
        return redirect('login')                        # переходим на страницу авторизации

# перевод заказа из статуса "корзина" в статус "заказ сформирован"
def make_order(request,order_id):
    oitems = OrderItems.objects.filter(order_id=order_id)   # получение перечня товаров в заказе
    for oi in oitems:                                   # перебор товара в заказе
        pr = Products.objects.get(pk=oi.item_id)        # получение объекта товара по ид из заказа
        pr.balance -= oi.i_count                        # уменьшение количества товара на остатке, на количество товара из заказа
        pr.save()                                       # созранение изменений по товару
    order = Orders.objects.get(pk=order_id)             # полученение объекта заказа
    order.box = False                                   # установка флага box в значение False, что озночает что заказ перешел
    order.save()                                        # из статуса "Корзина" в статус "заказ сформирован"
    return redirect('show_box',order_id)                # обновление страницы отображения заказа

# установка флага оплачено по заказу
def pay_order(request,order_id):
    order = Orders.objects.get(pk=order_id)             # получение объекта заказа
    order.pay_it = True                                 # перевод флага оплаты в значение True
    order.save()                                        # сохранение изменений
    return redirect('show_box',order_id)                # обновление страницы

# регистрация нового пользователя
class RegisterUser(DataMixin,CreateView):
    form_class = RegisterUserForm                       # указание стандартной формы регистрации
    template_name = 'main/register.html'                # привязка страницы к форме
    success_url = reverse_lazy('login')                 # при успешной регистрации, переход на форму авторизации
    def get_context_data(self, *, object_list=None, **kwargs):  # функция получения и обогащения контекста данных
        context = super().get_context_data(**kwargs)            # получение уже имеющихся данных
        c_def = self.get_user_context(title="Регистрация")      # формирование дополнительных данных
        return dict(list(context.items()) + list(c_def.items()))    # передаем обьединенный контекст переменных на страницу

def form_valid(self, form):                             # проверка на корректность заполненых данных
        user = form.save()                              # сохранение пользователя
        login(self.request, user)                       # авторизация под новым пользователем
        return redirect('det_user',user.pk)             # переход на страницу для заполнения дополнительных данных о пользователе

# авторизация пользоателя
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm                          # указание стандартной формы авторизации
    template_name = 'main/login.html'                   # привязка страницы к форме
    def get_context_data(self, *, object_list=None, **kwargs):  # функция получения и обогащения контекста данных
        context = super().get_context_data(**kwargs)            # получение уже имеющихся данных
        c_def = self.get_user_context(title="Авторизация")      # формирование дополнительных данных
        return dict(list(context.items()) + list(c_def.items()))    # передаем обьединенный контекст переменных на страницу

    def get_success_url(self):
        return reverse_lazy('home')                      # при успешной авторизации переход на главную страницу

# выход пользователя
def logout_user(request):
    logout(request)                                     # разлогиневание пользователя
    return redirect('login')                            # преход на страницу для авторизации

#================================ API ====================================
# вью сет для работы с API
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()                   # привязка вью сета к модели
    serializer_class = ProductSerializer                # привязка вью сета к сериалайзеру
    permission_classes = (IsAdminOrReadOnly,)           # подключение созданой модели пермишена

    @action(methods=['get'], detail=False)              # подключение возможности запроса данных о категориях товара (как связаной таблицы)
    def category(self,request):
        cats = PCategories.objects.all()                # получение queryset по всем категориям
        cat_dict = []                                   # фомирование переменной с пустым масивом
        for c in cats:                                  # перебор qveryseta категрий
            cat_dict.append({'id': c.id,'name': c.name})    # формирование данных в нужной форме, для отправки ответа
        return Response({'category': cat_dict})         # возврат ответа на запрос




