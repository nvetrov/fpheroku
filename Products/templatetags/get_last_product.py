from django import template
from Products.models import FoundGoods

register = template.Library()


@register.simple_tag(name='last_product')
def get_last_product():
    return FoundGoods.objects.order_by('id').last()
            # FoundGoods.objects.latest('id')
