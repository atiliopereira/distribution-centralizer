# -*- coding: utf-8 -*-
from django.db.models import Sum

from productos.models import Producto
from remisiones.forms import RemisionSearchForm
from remisiones.models import DetalleDeRemision
from remisiones.views import get_remisiones_queryset
from sistema.globales import separar, listview_to_excel


def lista_remisiones(request):
    form = RemisionSearchForm(request.GET)
    form.is_valid()

    desde = form.cleaned_data.get('desde', '')
    if desde:
        desde = desde.strftime("%d/%m/%Y")
    hasta = form.cleaned_data.get('hasta', '')
    if hasta:
        hasta = hasta.strftime("%d/%m/%Y")

    queryset = get_remisiones_queryset(request, form)
    nombre_archivo = 'lista_remisiones'
    titulos_productos = [producto.descripcion for producto in Producto.objects.filter(activo=True).order_by('id')]
    lista_datos = []
    cantidades_totales_por_producto = [0] * len(titulos_productos)
    for remision in queryset.order_by('fecha_de_emision'):
        cantidades = []
        for i, producto in enumerate(Producto.objects.filter(activo=True).order_by('id')):
            cantidad = DetalleDeRemision.objects.filter(remision=remision).filter(producto=producto).aggregate(
            Sum('cantidad')).get('cantidad__sum')
            if cantidad:
                cantidades.append(cantidad)
                cantidades_totales_por_producto[i] += cantidad
            else:
                cantidades.append(0)

        movil = '-'
        if remision.vehiculo:
            movil = remision.vehiculo.__str__()

        linea = [
            remision.fecha_de_emision.strftime("%d/%m/%Y"),
            remision.numero_de_remision,
            remision.punto_de_entrega.__str__(),
            movil,
            remision.get_estado_display(),
        ]
        linea.extend(cantidades)
        lista_datos.append(linea)
    totales_row = ['', '', '', 'Total']
    totales_row.extend(cantidades_totales_por_producto)
    lista_datos.append([])
    lista_datos.append(totales_row)
    lista_datos.append([])
    lista_datos.append(['Desde: ', desde, 'Hasta: ', hasta])
    titulos = ['Fecha', 'Numero de Remisión', 'Punto de entrega', 'Móvil', 'Estado']
    for titulo_producto in titulos_productos:
        titulos.append(titulo_producto)
    response = listview_to_excel(lista_datos, nombre_archivo, titulos)
    return response