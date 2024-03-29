# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.forms import Select
from django.utils.safestring import mark_safe
from django.contrib import messages

from remisiones.forms import RemisionSearchForm, RemisionForm
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
    list_display = ('editar', 'ver', 'numero_de_remision', 'fecha_de_emision', 'punto_de_entrega', 'estado',
                    'fecha_de_facturacion', 'anular',)
    list_filter = ('estado', )
    inlines = (DetalleDeRemisionInlineAdmin, )
    autocomplete_fields = ('punto_de_entrega', 'punto_de_partida', 'vehiculo', 'chofer', )
    actions = ('crear_factura_action', )
    form = RemisionForm
    fieldsets = (
        (None, {
            'fields': ('numero_de_remision', 'fecha_de_emision', )
        }),

        ('DESTINATARIO DE LA MERCADERIA', {
            'fields': ('punto_de_entrega', )
        }),

        ('DATOS DEL TRASLADO', {
            'fields': (
                ('motivo_del_traslado', 'comprobante_de_venta'),
                ('numero_de_comprobante_de_venta', 'numero_de_timbrado'),
                'fecha_de_expedicion',
                ('fecha_de_inicio_del_traslado', 'fecha_estimada_de_termino_del_traslado'),
                'punto_de_partida',
                'kilometros_estimados_de_recorrido',
                'cambio_de_fecha_de_termino_del_traslado_o_punto_de_llegada',
                'motivo',
            )
        }),

        ('DATOS DEL VEHICULO DE TRANSPORTE', {
            'fields': ('vehiculo', )
        }),

        ('DATOS DEL CONDUCTOR DEL VEHICULO', {
            'fields': ('chofer', )
        }),

    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def editar(self, obj):
        if obj.estado == EstadoDocumento.PENDIENTE:
            html = '<a href="/admin/remisiones/remision/%s" class="icon-block"> <i class="fa fa-edit"></i></a>' % obj.pk
        else:
            html = ''
        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/remisiones/remision_detail/%s" class="icon-block"> <i class="fa fa-eye"></i></a>' % obj.pk
        return mark_safe(html)

    def anular(self, obj):
        if obj.estado == EstadoDocumento.PENDIENTE:
            html = '<a href="/admin/remisiones/anular_remision/%s" class="icon-block"> <i class="fa fa-times-circle" style="color:red"></i></a>'  % obj.pk
        else:
            html = ''
        return mark_safe(html)

    def crear_factura_action(self, request, queryset):
        if all(queryset[0].punto_de_entrega.cliente == remision.punto_de_entrega.cliente and remision.estado == EstadoDocumento.PENDIENTE for remision in queryset):
            try:
                puntos = queryset.order_by('punto_de_entrega').distinct('punto_de_entrega').count()
                if puntos > 1:
                    venta = Venta.objects.create(numero_de_factura='000-000-0000000',
                                                 condicion_de_venta=CondicionDeVenta.CREDITO,
                                                 cliente=queryset[0].punto_de_entrega.cliente,
                                                 estado=EstadoDocumento.PENDIENTE)
                else:
                    venta = Venta.objects.create(numero_de_factura='000-000-0000000',
                                                 condicion_de_venta=CondicionDeVenta.CREDITO,
                                                 cliente=queryset[0].punto_de_entrega.cliente,
                                                 punto_de_entrega=queryset[0].punto_de_entrega,
                                                 estado=EstadoDocumento.PENDIENTE)
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
        form = getattr(self, 'advanced_search_form', None)
        if form:
            qs = get_remisiones_queryset(request, form)
        else:
            qs = super(RemisionAdmin, self).get_queryset()
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
