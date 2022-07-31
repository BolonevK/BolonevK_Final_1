from django import template
from ..models import *

register = template.Library()



@register.inclusion_tag('main/sel_cat.html')        # пользовательский тэг, для формирования списка категорий
def show_cat(sel_cat=0):
    cv = []
    cats = PCategories.objects.all()
    c1 = PCategories.objects.get(pk=1)
    print(c1.products_set.exists())
    for c in cats :
        if c.products_set.exists():
            cv.append(c)
    return {"cats": cv, "sel_cat": sel_cat}




