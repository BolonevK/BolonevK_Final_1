from django.db.models import Count

from .models import *

# menu = [{'title': "О сайте", 'url_name': 'about'},
#         {'title': "Добавить статью", 'url_name': 'add_page'},
#         {'title': "Обратная связь", 'url_name': 'contact'},
# ]

class DataMixin:
    # paginate_by = 2
    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu =  [{'title': "О сайте", 'url_name': 'about'},]
        if not self.request.user.is_authenticated:
            user_menu.append({'title': "Регистрация ", 'url_name': 'register'})
            user_menu.append({'title': "Войти ", 'url_name': 'login'})
        else:
            c_ord = Orders.objects.filter(user_id=self.request.user.pk)
            user_menu.append({'title': "Заказы: "+str(len(c_ord)), 'url_name': 'order_list'})
            user_menu.append({'title': self.request.user.username, 'url_name': 'order_list'})
            user_menu.append({'title': "Выйти", 'url_name': 'logout_user'},)
        context['menu'] = user_menu

        # context['cats'] = cats
        if 'sel_cat' not in context:
            context['sel_cat'] = 0
        return context