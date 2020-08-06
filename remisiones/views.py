# -*- coding: utf-8 -*-

from remisiones.models import Remision


def get_remisiones_queryset(request, form):
    qs = Remision.objects.all()
    estado = request.GET.get('estado__exact', '')
    if estado != '':
        qs = qs.filter(estado__exact=estado)
    if form.cleaned_data.get('numero', ''):
        qs = qs.filter(numero_de_remision__icontains=form.cleaned_data['numero'])
    if form.cleaned_data.get('cliente', ''):
        qs = qs.filter(cliente__razon_social__icontains=form.cleaned_data.get('cliente', ''))
    if form.cleaned_data.get('desde', ''):
        qs = qs.filter(fecha_de_emision__gte=form.cleaned_data.get('desde', ''))
    if form.cleaned_data.get('hasta', ''):
        qs = qs.filter(fecha_de_emision__lte=form.cleaned_data.get('hasta', ''))
    return qs

