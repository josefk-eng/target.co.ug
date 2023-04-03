from django import template

register = template.Library()


@register.filter
def ordered_products(id_string, product_list):
    strength = id_string.split('#')
    # return product_list.filter(id=)
