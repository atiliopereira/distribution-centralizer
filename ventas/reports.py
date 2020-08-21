# -*- coding: utf-8 -*-
from sistema.constants import EstadoDocumento
from sistema.globales import separar, listview_to_excel
from ventas.constants import CondicionDeVenta
from ventas.forms import VentaSearchForm
from ventas.models import RemisionEnVenta
from ventas.views import get_ventas_queryset


def lista_ventas(request):
    form = VentaSearchForm(request.GET)
    form.is_valid()

    desde = form.cleaned_data.get('desde', '')
    if desde:
        desde = desde.strftime("%d/%m/%Y")
    hasta = form.cleaned_data.get('hasta', '')
    if hasta:
        hasta = hasta.strftime("%d/%m/%Y")

    queryset = get_ventas_queryset(request, form)
    total = 0

    nombre_archivo = 'lista_ventas'

    lista_datos = []
    for venta in queryset.order_by('fecha_de_emision'):
        total += venta.total
        if venta.condicion_de_venta == CondicionDeVenta.CONTADO:
            condicion = 'Contado'
        elif venta.condicion_de_venta == CondicionDeVenta.CREDITO:
            condicion = 'Crédito'

        if venta.estado == EstadoDocumento.PENDIENTE:
            estado = 'Pendiente'
        elif venta.estado == EstadoDocumento.CONFIRMADO:
            estado = 'Pagado'

        remisiones_query = RemisionEnVenta.objects.filter(venta=venta)
        remisiones = ''
        if remisiones_query:
            for remision in remisiones_query:
                remisiones += f'{remision.remision.numero_de_remision}, '

        lista_datos.append([
            venta.fecha_de_emision.strftime("%d/%m/%Y"),
            venta.cliente.razon_social,
            venta.get_direccion(),
            condicion,
            estado,
            separar(int(venta.total)),
            remisiones,
        ])
    lista_datos.append([])
    lista_datos.append(['', '', '', 'Total', separar(int(total)),])
    lista_datos.append([])
    lista_datos.append(['Desde: ', desde, 'Hasta: ', hasta])
    titulos = ['Fecha', 'Cliente', 'Dirección', 'Condición', 'Estado', 'Monto', 'Remisiones']
    response = listview_to_excel(lista_datos, nombre_archivo, titulos)
    return response