from django.contrib import admin
from django.contrib.admin.decorators import register

from productos.models import Producto, ProductoCliente


@register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    search_fields = ('descripcion',)
    list_display = ('descripcion', 'precio', 'activo')
    actions = None


@register(ProductoCliente)
class ProductoClienteAdmin(admin.ModelAdmin):
    search_fields = ('cliente', 'producto', )
    list_display = ('producto', 'cliente', 'precio', 'fecha_de_creacion')
    list_filter = ('cliente__grupo',)
    autocomplete_fields = ('cliente', 'producto')
    actions = None