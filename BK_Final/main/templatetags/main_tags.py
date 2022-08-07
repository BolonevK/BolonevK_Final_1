from django import template
from ..models import *

register = template.Library()   # регистрация тэга

# пользовательский тэг, для формирования списка категорий
@register.inclusion_tag('main/sel_cat.html')    # указание страницы, на которую будет передача сформированых данных
def show_cat(sel_cat=0):                        # по умолчанию категория не выбрана
    cv = []                                     # формирование переменной с пустым массивом
    cats = PCategories.objects.all()            # получение queryset объектов категорий
    for c in cats :                             # перебор query set
        if c.products_set.exists():             # если существует товар с указанной категорией
            cv.append(c)                        # то добавляем категорию для отображения
    return {"cats": cv, "sel_cat": sel_cat}     # возврат сформированных данных




