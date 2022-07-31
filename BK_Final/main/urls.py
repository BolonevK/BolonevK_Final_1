from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('category/<int:cat_id>/', show_cat, name='category'),
    path('prod/<int:prod_id>/',show_prod, name='prod'),
    path('add_box/<int:prod_id>', add_box, name='add_box'),
    path('add_feedback/<int:prod_id>', add_feedback, name='add_feedback'),
    path('show_box/', show_box, name='show_box'),
    path('show_order/', show_order, name='show_order'),
    path('login/', login, name='login'),
    path('register/', login, name='register'),
    # path('register/', RegisterUser.as_view(), name='register'),


]


