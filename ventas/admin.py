from django.contrib import admin

from ventas.models import DetalleDeVenta, Venta


class DetalleDeVentaInlineAdmin(admin.TabularInline):
    model = DetalleDeVenta
    autocomplete_fields = ('producto', )
    extra = 0


class VentaAdmin(admin.ModelAdmin):
    list_display = ('fecha_de_emision', 'numero_de_factura', 'condicion_de_venta', 'cliente', 'estado', 'total')
    list_filter = ('condicion_de_venta', 'estado')
    inlines = (DetalleDeVentaInlineAdmin, )
    autocomplete_fields = ('cliente', )
    actions = None


admin.site.register(Venta, VentaAdmin)

