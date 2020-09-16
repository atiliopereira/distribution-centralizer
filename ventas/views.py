# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import DetailView
from django.db.models import Q

from productos.models import Producto
from remisiones.models import Remision, DetalleDeRemision
from sistema.constants import EstadoDocumento
from ventas.models import Venta, RemisionEnVenta, DetalleDeVenta


class VentaDetailView(DetailView):
    model = Venta
    template_name = "admin/ventas/venta/venta_detail.html"

    def get_context_data(self, **kwargs):
        context = super(VentaDetailView, self).get_context_data(**kwargs)
        context['detalles'] = DetalleDeVenta.objects.filter(venta=self.object).order_by('producto_id')
        context['remisiones'] = RemisionEnVenta.objects.filter(venta=self.object)
        context['detalles_con_productos_diferentes'] = DetalleDeVenta.objects.filter(venta=self.object).distinct('producto').order_by('producto_id')
        context['lista_de_productos'] = Producto.objects.filter(activo=True).order_by('id')
        remisiones = Remision.objects.filter(pk__in=[i.remision_id for i in RemisionEnVenta.objects.filter(venta=self.object)])
        detalles_de_remisiones = []
        for remision in remisiones:
            lista = DetalleDeRemision.objects.filter(remision=remision)
            for elemento in lista:
                detalles_de_remisiones.append(elemento)
        context['detalles_de_remisiones'] = detalles_de_remisiones
        return context


def get_ventas_queryset(request, form):
    qs = Venta.objects.all()
    estado = request.GET.get('estado', '')
    condicion_de_venta = request.GET.get('condicion_de_venta__exact', '')
    if estado != '':
        if estado == 'SAN':
            qs = qs.exclude(estado__exact=EstadoDocumento.ANULADO)
        else:
            qs = qs.filter(estado__exact=estado)
    if condicion_de_venta != '':
        qs = qs.filter(condicion_de_venta__exact=condicion_de_venta)
    if form.cleaned_data.get('numero', ''):
        qs = qs.filter(numero_de_factura__icontains=form.cleaned_data['numero'])
    if form.cleaned_data.get('remision', ''):
        qs = qs.filter(pk__in=[i.venta_id for i in RemisionEnVenta.objects.filter(
            remision__numero_de_remision__icontains=form.cleaned_data['remision'])])
    if form.cleaned_data.get('cliente', ''):
        qs = qs.filter(cliente__razon_social__icontains=form.cleaned_data.get('cliente', ''))
    if form.cleaned_data.get('punto_de_entrega', ''):
        qs = qs.filter(Q(punto_de_entrega__referencia__icontains=form.cleaned_data.get('punto_de_entrega', '')) | Q(
            punto_de_entrega__direccion__icontains=form.cleaned_data.get('punto_de_entrega', '')))
    if form.cleaned_data.get('desde', ''):
        qs = qs.filter(fecha_de_emision__gte=form.cleaned_data.get('desde', ''))
    if form.cleaned_data.get('hasta', ''):
        qs = qs.filter(fecha_de_emision__lte=form.cleaned_data.get('hasta', ''))
    return qs


def anular_venta(request, pk):
    venta = Venta.objects.get(pk=pk)
    if request.method == 'POST':
        venta.estado = EstadoDocumento.ANULADO
        venta.save()

        remisiones_en_venta = RemisionEnVenta.objects.filter(venta=venta)
        if remisiones_en_venta:
            for detalle in remisiones_en_venta:
                detalle.remision.estado = EstadoDocumento.PENDIENTE
                detalle.remision.save()

        return redirect('/admin/ventas/venta/')

    mensaje = f'¿Confirmar anulación de {venta}?'
    advertencia = f'ADVERTENCIA: esta acción no se puede revertir.'
    return render(request, 'admin/ventas/venta/venta_confirm.html', {'mensaje': mensaje, 'advertencia': advertencia})


def confirmar_venta(request, pk):
    venta = Venta.objects.get(pk=pk)
    if request.method == 'POST':
        venta.estado = EstadoDocumento.CONFIRMADO
        venta.save()
        remisiones_en_venta = RemisionEnVenta.objects.filter(venta=venta)
        for remision_en_venta in remisiones_en_venta:
            remision_en_venta.remision.fecha_de_facturacion = datetime.date.today()
            remision_en_venta.remision.save()

        return redirect('/admin/ventas/venta/')

    mensaje = f'¿Marcar {venta} como cobrada?'
    advertencia = f'ADVERTENCIA: esta acción no se puede revertir.'
    return render(request, 'admin/ventas/venta/venta_confirm.html', {'mensaje': mensaje, 'advertencia': advertencia})
