from django.contrib import admin
from django.utils.safestring import mark_safe

from sistema.constants import EstadoDocumento
from ventas.models import DetalleDeVenta, Venta


class DetalleDeVentaInlineAdmin(admin.TabularInline):
    model = DetalleDeVenta
    autocomplete_fields = ('producto',)
    extra = 0


class VentaAdmin(admin.ModelAdmin):
    list_display = (
    'fecha_de_emision', 'numero_de_factura', 'condicion_de_venta', 'cliente', 'estado', 'total', 'anular')
    list_filter = ('condicion_de_venta', 'estado')
    inlines = (DetalleDeVentaInlineAdmin,)
    autocomplete_fields = ('cliente',)
    actions = None

    def anular(self, obj):
        if obj.estado != EstadoDocumento.ANULADO:
            html = '<a href="/admin/ventas/anular_venta/%s" class="icon-block"> <i class="fa fa-times-circle" style="color:red"></i></a>' % obj.pk
        else:
            html = ''
        return mark_safe(html)

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Venta, VentaAdmin)
