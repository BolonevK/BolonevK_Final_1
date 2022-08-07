from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import admin


# модель категории продуктов
class PCategories(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория')     #   наименование категорий

    def __str__(self):                      # изменение стороки отображения элемента модели в queryset
        return self.name                    # устанавливаем в качестве отображение ниаменование категории

    def get_absolute_url(self):             # получение абсолютного адреса для объекта модели
        return reverse('category', kwargs={'cat_id': self.pk})  # фомирование адреса с учетом переданной переменной

    class Meta:                             # установка значений для отображения модели в админ панели
        verbose_name = 'Категория'          # установка наименования еденичного числа модели
        verbose_name_plural = 'Категории'   # установка наименования множественного числа модели
        ordering = ['id']                   # установка сортировки для отображения элементов модели

# модель продуктов(товаров)
class Products(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')        # наименование товара
    factory = models.CharField(max_length=250, verbose_name='Производитель')    # производитель товара
    p_text = models.TextField(verbose_name='Описание')                          # полное описание товара
    image = models.ImageField(upload_to='media/', null=True, default='media/prod_none.png', verbose_name='Изображение')        # картинка товара
    balance = models.IntegerField(verbose_name='Остаток')        #  остаток на складе
    coast = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')         #  цена товара
    cat = models.ForeignKey(PCategories, on_delete=models.PROTECT, verbose_name='Категория')       #  категория к которой принадлежит товар

    def __str__(self):                      # изменение стороки отображения элемента модели в queryset
        return self.name                    # устанавливаем в качестве отображение ниаменование товара

    def get_absolute_url(self):     # cтандартная функция получения абсолютной ссылки
        return reverse('prod', kwargs={'prod_id': self.pk})     # фомирование адреса с учетом переданной переменной

    class Meta:                             # установка значений для отображения модели в админ панели
        verbose_name = 'Товар'              # установка наименования еденичного числа модели
        verbose_name_plural = 'Товары'      # установка наименования множественного числа модели
        ordering = ['id']                   # установка сортировки для отображения элементов модели

# модель клиента, в ней хранятся дополнительные данные о клиенте
class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)         # ссылка на встроеный класс User
    phone = models.CharField(max_length=12)                             # телефон клиента
    address = models.CharField(max_length=200)                          # адрес клиента

# модель заказа
class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)            # ссылка на клиента
    date_create = models.DateTimeField(auto_now_add=True)               # дата создания заказа (устанавливается автоматом текущей датой)
    coast = models.DecimalField(max_digits=10, decimal_places=2)        # Стоимость всего заказа
    pay_it = models.BooleanField(default=False)                         # флаг оплаты, показывает оплачен заказ или нет
    transfer = models.BooleanField(default=False)                       # флаг отгрузки, показывает отгружен ли товар
    box = models.BooleanField(default=True)     # флаг корзины, показывает является ли заказ еще "корзиной" или оформленым заказом.

    def get_absolute_url(self):     # cтандартная функция получения абсолютной ссылки
        return reverse('make_order', kwargs={'order_id': self.pk})      # фомирование адреса с учетом переданной переменной

    @admin.display(description='Client address')                        # фомирование адреса для админ панели, в раздел Заказы
    def Cl_address(self):                                               # фомирование метода для получения адреса
        return Clients.objects.get(user_id= self.user.pk).address       # полечение адреса для админ панели

    @admin.display(description='Client phone')                          # фомирование телефона для админ панели, в раздел Заказы
    def Cl_phone(self):                                                 # формирование метода для получения телефона
        return Clients.objects.get(user_id= self.user.pk).phone         # полечение адреса для админ панели

    class Meta:                             # установка значений для отображения модели в админ панели
        verbose_name = 'Заказ'              # установка наименования еденичного числа модели
        verbose_name_plural = 'Заказы'      # установка наименования множественного числа модели
        ordering = ['id']                   # установка сортировки для отображения элементов модели

# модель компонентов заказа
class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)         # ссылка на заказ
    item = models.ForeignKey(Products, on_delete=models.CASCADE)        # ссыдка на товар
    i_count = models.IntegerField()                                     # количество товара
    # deleted = models.BooleanField(default=False)

# модель отзывов о товаре
class FeedBack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)            # ссылка на клиента
    product = models.ForeignKey(Products, on_delete=models.CASCADE)     # ссылка на товар
    fb_text = models.TextField()                                        # текст отзыва
    fb_mark = models.IntegerField()                                     # оценка отзыва

