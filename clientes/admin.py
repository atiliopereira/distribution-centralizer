from django.contrib import admin
from django.contrib.admin.decorators import register

from clientes.models import Cliente, PuntoEntregaCliente


class PuntoEntregaClienteInline(admin.TabularInline):
    model = PuntoEntregaCliente
    extra = 0


@register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('razon_social', 'ruc', 'direccion', 'telefono', 'email',)
    list_display = ('razon_social', 'ruc', 'direccion', 'telefono', 'email', 'dia_de_presentacion', 'activo')
    inlines = (PuntoEntregaClienteInline, )
    actions = None
