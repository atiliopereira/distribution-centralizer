from django.contrib import admin
from django.contrib.admin.decorators import register
from django.utils.safestring import mark_safe

from clientes.models import Cliente, PuntoEntregaCliente


class PuntoEntregaClienteInline(admin.TabularInline):
    model = PuntoEntregaCliente
    extra = 0


@register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('razon_social', 'ruc', 'direccion', 'telefono', 'email',)
    list_display = ('razon_social', 'ruc', 'direccion', 'telefono', 'email', 'dia_de_presentacion', 'activo',
                    'get_deuda', 'get_remisiones_pendientes', 'ver')
    inlines = (PuntoEntregaClienteInline, )
    actions = None

    def ver(self, obj):
        html = '<a href="/admin/clientes/cliente_detail/%s" class="icon-block"> <i class="fa fa-eye"></i></a>' % obj.pk
        return mark_safe(html)