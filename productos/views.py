from django.shortcuts import render

from productos.models import ProductoCliente


def get_productoscliente_queryset(request, form):
    qs = ProductoCliente.objects.all()
    if form.cleaned_data.get('producto', ''):
        qs = qs.filter(producto__descripcion__icontains=form.cleaned_data['producto'])
    if form.cleaned_data.get('cliente', ''):
        qs = qs.filter(cliente__razon_social__icontains=form.cleaned_data.get('cliente', ''))
    if form.cleaned_data.get('desde', ''):
        qs = qs.filter(fecha_de_creacion__gte=form.cleaned_data.get('desde', ''))
    if form.cleaned_data.get('hasta', ''):
        qs = qs.filter(fecha_de_creacion__lte=form.cleaned_data.get('hasta', ''))
    return qs
