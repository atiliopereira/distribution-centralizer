from django.contrib import admin
from django.contrib.admin.decorators import register

from clientes.models import Cliente, Grupo


@register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)
    list_display = ('nombre', 'dia_de_presentacion')


@register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('razon_social', 'ruc',)
    list_display = ('razon_social', 'ruc', 'direccion', 'telefono', 'email', 'activo')
    list_filter = ('grupo', 'activo')
    autocomplete_fields = ('grupo', )
    actions = None
