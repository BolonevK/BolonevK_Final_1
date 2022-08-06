from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers  # router для API

router = routers.DefaultRouter()
# router = routers.SimpleRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    # path('', index, name='home'),
    path('', MarketMain.as_view(), name='home'),
    path('about/', about, name='about'),
    path('admin/', admin_panel, name='admin'),
    # path('category/<int:cat_id>/', show_cat, name='category'),
    path('category/<int:cat_id>/', ShowCat.as_view(), name='category'),
    # path('prod/<int:prod_id>/',show_prod, name='prod'),
    path('prod/<int:prod_id>/',ShowProd.as_view(), name='prod'),
    path('add_box/<int:prod_id>', add_box, name='add_box'),
    path('del_box/<int:prod_id>', del_box, name='del_box'),
    path('add_feedback/<int:prod_id>', add_feedback, name='add_feedback'),
    # path('add_feedback/<int:prod_id>', Add_Feedback.as_view(), name='add_feedback'),
    # path('show_box/', show_box, name='show_box'),
    path('show_box/<int:order_id>/', ShowBox.as_view(), name='show_box'),
    path('det_user/<int:user_id>/', det_user, name='det_user'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout_user'),
    # path('register/', register, name='register'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('make_order/<int:order_id>', make_order, name='make_order'),
    path('pay_order/<int:order_id>', pay_order, name='pay_order'),
    path('order_list/', OrderList.as_view(), name='order_list'),
# Для работы через API

    path('api/', include(router.urls)),
    # path('api/crud_prod/', ProductViewSet.as_view({'get' : 'list'})),
    # path('api/crud_prod/<int:pk>/', ProductViewSet.as_view({'put' : 'update'})),
    # path('api/crud_prod/', ProductAPI_RC.as_view()),
    # path('api/crud_prod/<int:pk>/', ProductAPI_RUD.as_view()),



]


