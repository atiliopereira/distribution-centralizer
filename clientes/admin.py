from django.contrib import admin
from django.utils.safestring import mark_safe

from clientes.models import Cliente, PuntoEntregaCliente


class PuntoEntregaClienteAdmin(admin.ModelAdmin):
    search_fields = ('referencia', 'direccion', 'cliente__razon_social',)
    list_display = ('referencia', 'direccion', 'cliente', 'ciudad', 'departamento',)
    list_filter = ('ciudad', 'departamento', )
    actions = None

admin.site.register(PuntoEntregaCliente, PuntoEntregaClienteAdmin)


class PuntoEntregaClienteInline(admin.TabularInline):
    model = PuntoEntregaCliente
    autocomplete_fields = ('ciudad', 'departamento', )
    extra = 0


class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('razon_social', 'ruc', 'direccion', 'telefono', 'email',)
    list_display = ('razon_social', 'ruc', 'direccion', 'telefono', 'email', 'dia_de_presentacion',
                    'get_deuda', 'get_remisiones_pendientes', 'ver', 'activo',)
    inlines = (PuntoEntregaClienteInline, )
    actions = None

    def ver(self, obj):
        html = '<a href="/admin/clientes/cliente_detail/%s" class="icon-block"> <i class="fa fa-eye"></i></a>' % obj.pk
        return mark_safe(html)


admin.site.register(Cliente, ClienteAdmin)