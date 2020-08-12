# -*- coding: utf-8 -*-
import datetime

from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import DetailView

from productos.models import ProductoCliente, Producto, get_precio
from ventas.models import DetalleDeVenta


class ProductoDetailView(DetailView):
    model = Producto
    template_name = "admin/productos/producto/producto_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductoDetailView, self).get_context_data(**kwargs)
        precios_actuales = []
        for productocliente in ProductoCliente.objects.filter(producto=self.object).filter(cliente__activo=True).distinct(
            'cliente').order_by('cliente_id'):
            precio = get_precio(productocliente.cliente, productocliente.producto, fecha=datetime.date.today())
            elemento = [productocliente.cliente, precio]
            precios_actuales.append(elemento)
        context['productos_por_cliente'] = precios_actuales
        context['productos_vendidos'] = DetalleDeVenta.objects.filter(producto=self.object).aggregate(
            Sum('cantidad')).get('cantidad__sum')
        return context


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
