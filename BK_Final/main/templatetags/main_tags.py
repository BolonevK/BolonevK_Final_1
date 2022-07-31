from django import template
from ..models import *

register = template.Library()



@register.inclusion_tag('main/sel_cat.html')        # пользовательский тэг, для формирования списка категорий
def show_cat(sel_cat=0):
    cats = PCategories.objects.all()
    return {"cats": cats, "sel_cat": sel_cat}

@register.simple_tag()
def add_box(prod_id):
    print('it is worked')

