from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers  # router для API

router = routers.DefaultRouter()                 # подключение ройтера, для работы через API
router.register(r'product', ProductViewSet)      # регистрация пути для работы API

urlpatterns = [
    path('', MarketMain.as_view(), name='home'),    # путь главной страницы
    path('about/', about, name='about'),            # путь страницы "о проекте"
    path('admin/', admin_panel, name='admin'),      # путь для админ панели
    path('category/<int:cat_id>/', ShowCat.as_view(), name='category'), # путь для отображения определенной категории
    path('prod/<int:prod_id>/',ShowProd.as_view(), name='prod'),    # путь для отображени информации по конкретному товару
    path('add_box/<int:prod_id>', add_box, name='add_box'),         # путь для добавления товара
    path('del_box/<int:prod_id>', del_box, name='del_box'),         # путь для удаления товара
    path('add_feedback/<int:prod_id>', add_feedback, name='add_feedback'),  # путь для дабавления отзыва
    path('show_box/<int:order_id>/', ShowBox.as_view(), name='show_box'),   # путь отображения информации о заказе
    path('det_user/<int:user_id>/', det_user, name='det_user'),     # путь формы ввода дополнительных данных
    path('login/', LoginUser.as_view(), name='login'),              # путь фомы для авторизации пользователя
    path('logout/', logout_user, name='logout_user'),               # путь разлогинивания пользователя
    path('register/', RegisterUser.as_view(), name='register'),         # путь формы регистрации нового пользователя
    path('make_order/<int:order_id>', make_order, name='make_order'),   # путь перевода статуса заказа
    path('pay_order/<int:order_id>', pay_order, name='pay_order'),      # путь для изменения флага "оплата" по заказу
    path('order_list/', OrderList.as_view(), name='order_list'),    # путь выводи списка заказов по авторизированому пользователю
# Для работы через API
    path('api/', include(router.urls)),             # путь для работы через API

]


