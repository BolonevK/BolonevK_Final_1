from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib import admin



class PCategories(models.Model):        #  класс категории продуктов
    name = models.CharField(max_length=50, verbose_name='Категория')     #   наименование категорий

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

class Products(models.Model):         # класс продуктов(товаров)
    name = models.CharField(max_length=100, verbose_name='Наименование')      # наименование товара
    factory = models.CharField(max_length=250, verbose_name='Производитель')       #  производитель товара
    p_text = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='media/', null=True, default='media/prod_none.png', verbose_name='Изображение')        # картинка товара
    balance = models.IntegerField(verbose_name='Остаток')        #  остаток на складе
    coast = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')         #  цена товара
    cat = models.ForeignKey(PCategories, on_delete=models.PROTECT, verbose_name='Категория')       #  категория к которой принадлежит товар

    def __str__(self):
        return self.name

    def get_absolute_url(self):     # cтандартная функция получения абсолютной ссылки
        return reverse('prod', kwargs={'prod_id': self.pk})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id']


class Clients(models.Model):         # клиент
    user = models.OneToOneField(User, on_delete=models.CASCADE)      #  ссылка на встроеный класс User
    phone = models.CharField(max_length=12)      # телефон клиента
    address = models.CharField(max_length=200)        #  адрес клиента


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # ссылка на клиента
    date_create = models.DateTimeField(auto_now_add=True)   # дата создания заказа (устанавливается автоматом текущей датой)
    coast = models.DecimalField(max_digits=10, decimal_places=2)    # Стоимость всего заказа
    pay_it = models.BooleanField(default=False)     # флаг оплаты, показывает оплачен заказ или нет
    transfer = models.BooleanField(default=False)       # флаг отгрузки, показывает отгружен ли товар
    box = models.BooleanField(default=True)     # флаг корзины, показывает является ли заказ еще корзиной или оформленым заказом.

    def get_absolute_url(self):     # cтандартная функция получения абсолютной ссылки
        return reverse('make_order', kwargs={'order_id': self.pk})

    @admin.display(description='Client address')
    def Cl_address(self):
        return Clients.objects.get(user_id= self.user.pk).address

    @admin.display(description='Client phone')
    def Cl_phone(self):
        return Clients.objects.get(user_id= self.user.pk).phone
class OrderItems(models.Model):     # класс компонет заказа
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)        # ссылка на заказ
    item = models.ForeignKey(Products, on_delete=models.CASCADE)       # ссыдка на товар
    i_count = models.IntegerField()        # количество товара
    deleted = models.BooleanField(default=False)


class FeedBack(models.Model):       # класс отзыва о товаре
    user = models.ForeignKey(User, on_delete=models.CASCADE)       # ссылка на клиента
    product = models.ForeignKey(Products, on_delete=models.CASCADE)       # ссылка на товар
    fb_text = models.TextField()       # текст отзыва
    fb_mark = models.IntegerField()       # оценка отзыва

