# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib import messages

from remisiones.forms import RemisionSearchForm
from remisiones.models import DetalleDeRemision, Remision
from remisiones.views import get_remisiones_queryset
from sistema.constants import EstadoDocumento
from ventas.constants import CondicionDeVenta
from ventas.models import Venta, RemisionEnVenta


class DetalleDeRemisionInlineAdmin(admin.TabularInline):
    model = DetalleDeRemision
    autocomplete_fields = ('producto', )
    extra = 0


class RemisionAdmin(admin.ModelAdmin):
    list_display = ('editar', 'numero_de_remision', 'fecha_de_emision', 'fecha_de_facturacion', 'cliente', 'chofer', 'vehiculo', 'estado', 'anular')
    list_filter = ('estado', )
    inlines = (DetalleDeRemisionInlineAdmin, )
    autocomplete_fields = ('cliente', 'ciudad_de_partida', 'ciudad_de_llegada', 'vehiculo', 'chofer', )
    actions = ('crear_factura_action', )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def editar(self, obj):
        html = '<a href="/admin/remisiones/remision/%s" class="icon-block"> <i class="fa fa-edit"></i></a>'  % obj.pk
        return mark_safe(html)

    def anular(self, obj):
        html = '<a href="/admin/remisiones/remision/%s" class="icon-block"> <i class="fa fa-times-circle" style="color:red"></i></a>'  % obj.pk
        return mark_safe(html)

    def crear_factura_action(self, request, queryset):
        if all(queryset[0].cliente.razon_social == remision.cliente.razon_social and remision.estado == EstadoDocumento.PENDIENTE for remision in queryset):
            try:
                venta = Venta.objects.create(numero_de_factura='COMPLETAR', condicion_de_venta=CondicionDeVenta.CREDITO,
                                             cliente=queryset[0].cliente, estado=EstadoDocumento.PENDIENTE)
                for remision in queryset:
                    RemisionEnVenta.objects.create(venta=venta, remision=remision)

                datos = {
                    's': 's' if len(queryset) > 1 else '',
                    'es': 'es' if len(queryset) > 1 else '',
                    'remisiones': " - ".join(map(str, queryset))
                }
                self.message_user(request, mark_safe(
                    u'Factura de venta creada con la{s} remision{es} "<strong>{remisiones}</strong>"'.format(**datos)),
                                  messages.INFO)

            except Exception as e:
                self.message_user(request, mark_safe(
                    u'Ocurrió un error al crear la factura de venta. Error: %s' % str(e)), messages.ERROR)

        else:
            self.message_user(request, mark_safe(
                u'Las remisiones deben ser de un único cliente y estar en estado pendiente.'), messages.ERROR)

    crear_factura_action.short_description = "Crear Factura con remision/es seleccionada/s"

    def get_queryset(self, request):
        form = self.advanced_search_form
        qs = get_remisiones_queryset(request, form)
        return qs

    def changelist_view(self, request, extra_context=None, **kwargs):
        self.my_request_get = request.GET.copy()
        self.advanced_search_form = RemisionSearchForm(request.GET)
        self.advanced_search_form.is_valid()
        self.other_search_fields = {}
        params = request.get_full_path().split('?')

        extra_context = extra_context or {}
        extra_context.update({'asf': RemisionSearchForm,
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

        return super(RemisionAdmin, self) \
            .changelist_view(request, extra_context=extra_context, **kwargs)


admin.site.register(Remision, RemisionAdmin)
