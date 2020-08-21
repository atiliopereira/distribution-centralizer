from django.contrib import admin
from django.utils.safestring import mark_safe

from sistema.constants import EstadoDocumento
from sistema.globales import separar
from ventas.forms import VentaSearchForm, VentaForm
from ventas.models import DetalleDeVenta, Venta
from ventas.views import get_ventas_queryset


class DetalleDeVentaInlineAdmin(admin.TabularInline):
    model = DetalleDeVenta
    extra = 0


class VentaAdmin(admin.ModelAdmin):
    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js', 'js/admin/venta/change_form.js',)

    form = VentaForm
    list_display = ('editar', 'fecha_de_emision', 'numero_de_factura', 'condicion_de_venta', 'cliente', 'get_direccion',
                    'estado', 'total', 'acciones', 'ver', 'anular',)
    list_filter = ('condicion_de_venta', 'estado')
    inlines = (DetalleDeVentaInlineAdmin,)
    autocomplete_fields = ('cliente',)
    actions = None

    def editar(self, obj):

        if obj.estado == EstadoDocumento.PENDIENTE and obj.tiene_remisiones == 0:
            html = '<a href="/admin/ventas/venta/%s" class="icon-block"> <i class="fa fa-edit"></i></a>' % obj.pk
        else:
            html = ''
        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/ventas/venta_detail/%s" class="icon-block"> <i class="fa fa-eye"></i></a>' % obj.pk
        return mark_safe(html)

    def anular(self, obj):
        if obj.estado != EstadoDocumento.ANULADO:
            html = '<a href="/admin/ventas/anular_venta/%s" class="icon-block"> <i class="fa fa-times-circle" style="color:red"></i></a>' % obj.pk
        else:
            html = ''
        return mark_safe(html)

    def acciones(self, obj):
        if obj.estado == EstadoDocumento.PENDIENTE:
            html = '<a href="/admin/ventas/confirmar_venta/%s">Marcar como pagado</a>' % obj.pk
        else:
            html = ''
        return mark_safe(html)

    def has_delete_permission(self, request, obj=None):
        return False

    def lookup_allowed(self, lookup, *args, **kwargs):
        if lookup in self.advanced_search_form.fields.keys():
            return True
        return super(VentaAdmin, self).lookup_allowed(lookup, *args, **kwargs)

    def get_queryset(self, request):
        form = self.advanced_search_form
        qs = get_ventas_queryset(request, form)
        return qs

    def changelist_view(self, request, extra_context=None, **kwargs):
        self.my_request_get = request.GET.copy()
        self.advanced_search_form = VentaSearchForm(request.GET)
        self.advanced_search_form.is_valid()
        self.other_search_fields = {}
        params = request.get_full_path().split('?')

        ventas_queryset = self.get_queryset(request)
        total_ventas = 0
        for venta in ventas_queryset:
            total_ventas += venta.total

        extra_context = extra_context or {}
        extra_context.update({'asf': VentaSearchForm,
                              'total': separar(int(round(total_ventas))),
                              'my_request_get': self.my_request_get,
                              'params': '?%s' % params[1].replace('%2F', '/') if len(params) > 1 else ''
                              })
        request.GET._mutable = True

        for key in self.advanced_search_form.fields.keys():
            try:
                temp = request.GET.pop(key)
            except KeyError:
                pass
            else:
                if temp != ['']:
                    self.other_search_fields[key] = temp
        request.GET_mutable = False

        return super(VentaAdmin, self) \
            .changelist_view(request, extra_context=extra_context, **kwargs)


admin.site.register(Venta, VentaAdmin)
