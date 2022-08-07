from django.db.models import Count, Sum

from .models import *

# Миксима для формирования главного меню
class DataMixin:
    def get_user_context(self, **kwargs):       # получаем данные по запросу
        context = kwargs                        # фомирование переменной контекста
        user_menu =  [{'title': "О проекте", 'url_name': 'about'},]     # формирование переменной меню
        if not self.request.user.is_authenticated:                      # если пользователь не авторизован
            user_menu.append({'title': "Регистрация ", 'url_name': 'register'})     # добавляем пункты меню для регистрации пользователя
            user_menu.append({'title': "Войти ", 'url_name': 'login'})              # добавляем пункты меню для авторизации пользователя
        elif self.request.user.is_staff:        # если пользователь авторизован и является администратором
            user_menu.append({'title': 'Логин : ' + self.request.user.username, 'url_name': 'order_list'})  # добавляем пункты меню с указанием логина администратора
            user_menu.append({'title': "Админ панель ", 'url_name': 'admin'})       # добавляем пункты меню для перехода к админ панели
        else:                                   # если пользователь авторизован
            try:                                # пробуем получить заказ пользователя, который является "корзиной"
                n_ord = Orders.objects.get(user_id=self.request.user.pk, box=True)      # получаем номер заказа пользователя со статусом "корзина"
                box_items = OrderItems.objects.filter(order=n_ord.pk, i_count__gt=0)    # получаем товары, которые находятся в корзине
                cnt = box_items.aggregate(c_item=Sum('i_count'))    # получаем количество товара в корзине
                c_item = cnt['c_item']          # записываем количество товара в отдельную переменную
            except:                             # если у пользователя нет заказа в статусе "корзина"
                c_item = 0                      # устанавливаем значение 0 в переменную, которая показывает количество товара
            if (c_item == 0) or (c_item is None):   # проверяем есть ли в корзине товар
                user_menu.append({'title': "Корзина: 0", 'url_name': 'order_list', 'b_num' : 0})    # если нет, добавляем пунки меню "Корзина" со значением 0, и URLадрес на order_list
            else:                               # если товар в корзине есть
                user_menu.append({'title': "Корзина: "+str(c_item), 'url_name': 'show_box', 'b_num' : n_ord.pk })   # если товар есть, добавляем пунки меню "Корзина" с указанием количества товара, и URLадрес на show_box
            user_menu.append({'title': 'Логин : '+self.request.user.username, 'url_name': 'order_list'})    # добавляем пункт меню с указанием логина пользователя
        user_menu.append({'title': "Выйти", 'url_name': 'logout_user'},)    # добавляем пункт меню для выхода пользователя
        context['menu'] = user_menu             # добавляем переменную menu к контексту переменных

        if 'sel_cat' not in context:            # если в контексте отсутствует переменная, которая указывает на выбранную категорию
            context['sel_cat'] = 0              # устанавливаем ее в значение 0, для отображения всего списка товаров
        return context                          # возвращаем обогощенный контекст переменных обратно