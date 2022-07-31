from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id' , 'name', 'factory', 'p_text', 'image', 'balance', 'coast', 'cat')
    list_display_links = ('id' , 'name')
    search_fields = ('id' , 'name')

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id' , 'name')
    list_display_links = ('id' , 'name')
    search_fields = ('name',)

admin.site.register(Products,ProductAdmin)
admin.site.register(PCategories,CategoriesAdmin)