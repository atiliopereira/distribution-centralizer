# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import DetailView
from django.db.models import Q

from remisiones.models import Remision, DetalleDeRemision
from sistema.constants import EstadoDocumento


class RemisionDetailView(DetailView):
    model = Remision
    template_name = "admin/remisiones/remision/remision_detail.html"

    def get_context_data(self, **kwargs):
        context = super(RemisionDetailView, self).get_context_data(**kwargs)
        context['detalles'] = DetalleDeRemision.objects.filter(remision=self.object)
        return context


def get_remisiones_queryset(request, form):
    qs = Remision.objects.all()
    estado = request.GET.get('estado__exact', '')
    if estado != '':
        qs = qs.filter(estado__exact=estado)
    if form.cleaned_data.get('numero', ''):
        qs = qs.filter(numero_de_remision__icontains=form.cleaned_data['numero'])
    if form.cleaned_data.get('cliente', ''):
        qs = qs.filter(punto_de_entrega__cliente__razon_social__icontains=form.cleaned_data.get('cliente', ''))
    if form.cleaned_data.get('punto_de_entrega', ''):
        qs = qs.filter(Q(punto_de_entrega__referencia__icontains=form.cleaned_data.get('punto_de_entrega', '')) | Q(
            punto_de_entrega__direccion__icontains=form.cleaned_data.get('punto_de_entrega', '')))
    if form.cleaned_data.get('desde', ''):
        qs = qs.filter(fecha_de_emision__gte=form.cleaned_data.get('desde', ''))
    if form.cleaned_data.get('hasta', ''):
        qs = qs.filter(fecha_de_emision__lte=form.cleaned_data.get('hasta', ''))
    return qs


def anular_remision(request, pk):
    remision = Remision.objects.get(pk=pk)
    if request.method == 'POST':
        remision.estado = EstadoDocumento.ANULADO
        remision.fecha_de_facturacion = None
        remision.save()

        return redirect('/admin/remisiones/remision/')

    mensaje = f'¿Confirmar anulación de {remision}?'
    advertencia = f'ADVERTENCIA: esta acción no se puede revertir.'
    return render(request, 'admin/remisiones/remision/remision_confirm.html', {'mensaje': mensaje, 'advertencia': advertencia})
