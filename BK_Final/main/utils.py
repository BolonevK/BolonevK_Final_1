from django.db.models import Count, Sum

from .models import *

class DataMixin:
    # paginate_by = 2
    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu =  [{'title': "О проекте", 'url_name': 'about'},]
        if not self.request.user.is_authenticated:
            user_menu.append({'title': "Регистрация ", 'url_name': 'register'})
            user_menu.append({'title': "Войти ", 'url_name': 'login'})
        else:
            try:
                n_ord = Orders.objects.get(user_id=self.request.user.pk, box=True)
                box_items = OrderItems.objects.filter(order=n_ord.pk, i_count__gt=0)
                cnt = box_items.aggregate(c_item=Sum('i_count'))
                c_item = cnt['c_item']
            except:
                c_item = 0
            if (c_item == 0) or (c_item is None):
                user_menu.append({'title': "Корзина: 0", 'url_name': 'order_list', 'b_num' : 0})
            else:
                user_menu.append({'title': "Корзина: "+str(c_item), 'url_name': 'show_box', 'b_num' : n_ord.pk })
            user_menu.append({'title': 'Логин : '+self.request.user.username, 'url_name': 'order_list'})
            user_menu.append({'title': "Выйти", 'url_name': 'logout_user'},)
        context['menu'] = user_menu

        if 'sel_cat' not in context:
            context['sel_cat'] = 0
        return context