# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.template import RequestContext

from sistema.constants import EstadoDocumento
from ventas.models import Venta, RemisionEnVenta


def get_ventas_queryset(request, form):
    qs = Venta.objects.all()
    estado = request.GET.get('estado__exact', '')
    condicion_de_venta = request.GET.get('condicion_de_venta__exact', '')
    if estado != '':
        qs = qs.filter(estado__exact=estado)
    if condicion_de_venta != '':
        qs = qs.filter(condicion_de_venta__exact=condicion_de_venta)
    if form.cleaned_data.get('numero', ''):
        qs = qs.filter(numero_de_factura__icontains=form.cleaned_data['numero'])
    if form.cleaned_data.get('cliente', ''):
        qs = qs.filter(cliente__razon_social__icontains=form.cleaned_data.get('cliente', ''))
    if form.cleaned_data.get('remision', ''):
        qs = qs.filter(pk__in=[i.venta_id for i in RemisionEnVenta.objects.filter(
            remision__numero_de_remision__icontains=form.cleaned_data['remision'])])
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
