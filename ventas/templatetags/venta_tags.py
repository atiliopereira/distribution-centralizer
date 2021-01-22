from __future__ import unicode_literals
from django import template

from remisiones.templatetags.remision_tags import advanced_search_form

register = template.Library()


@register.inclusion_tag('admin/ventas/venta/venta_search_form.html', takes_context=True)
def venta_search_form(context, cl):
    return advanced_search_form(context, cl)


@register.filter
def eliminar_separador_miles(numero):
    numero_str = str(numero)
    return numero_str