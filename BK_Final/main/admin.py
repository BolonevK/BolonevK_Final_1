from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):                   # отображение в админ панели данных о товаре
    list_display = ('id' , 'name', 'factory', 'p_text', 'image', 'balance', 'coast', 'cat') # указываем поля для отображения
    list_display_links = ('id' , 'name')                # указываем поля, по которым можно будет открыть товар для редактирования
    search_fields = ('id' , 'name')                     # указываем поля, по которым можно будет осуществлять поиск товара

class CategoriesAdmin(admin.ModelAdmin):                # отображение в админ панели данных о категориях товаров
    list_display = ('id' , 'name')                      # указываем поля для отображения
    list_display_links = ('id' , 'name')                # указываем поля, по которым можно будет открыть категорию для редактирования
    search_fields = ('name',)                           # указываем поля, по которым можно будет осуществлять поиск категории

class OrderAdmin(admin.ModelAdmin):                     # отображение в админ панели данных о заказах
    list_display = ('id' , 'user', 'Cl_address', 'Cl_phone', 'date_create', 'coast', 'pay_it', 'transfer', 'box')    # указываем поля для отображения из модели Orders и данных из модели Clients
    list_display_links = ('id' , 'user')                # указываем поля, по которым можно будет открыть заказы для редактирования
    search_fields = ('user', 'pey_it', 'date_create')   # указываем поля, по которым можно будет осуществлять поиск категории

admin.site.register(Products,ProductAdmin)              # регистрируем форму отображения справочников товаров в админ панели
admin.site.register(PCategories,CategoriesAdmin)        # регистрируем форму отображения справочников категирии товаров в админ панели
admin.site.register(Orders,OrderAdmin)                  # регистрируем форму отображения справочников заказов в админ панели