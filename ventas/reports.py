# -*- coding: utf-8 -*-
import math
from io import BytesIO

from django.http import HttpResponse
from django.utils.encoding import force_text
from reportlab.pdfgen import canvas

from sistema.constants import EstadoDocumento
from sistema.globales import separar, listview_to_excel, numero_to_letras
from ventas.constants import CondicionDeVenta, Iva
from ventas.forms import VentaSearchForm
from ventas.models import RemisionEnVenta, DetalleDeVenta, Venta
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


def factura_pdf(request, id):
    def contenido(canvas, venta):
        from reportlab.lib.colors import darkblue, black
        from reportlab.lib.pagesizes import GOV_LEGAL

        canvas.setFillColor(darkblue)
        canvas.setFillColor(black)
        canvas.setStrokeColor(black)
        canvas.setFont("Helvetica", 10)
        canvas.setPageSize(GOV_LEGAL)

        canvas.drawString(102, 851, force_text(venta.fecha_de_emision.strftime('%d/%m/%Y') or ''))
        canvas.drawString(102, 528, force_text(venta.fecha_de_emision.strftime('%d/%m/%Y') or ''))
        canvas.drawString(102, 205, force_text(venta.fecha_de_emision.strftime('%d/%m/%Y') or ''))
        if venta.condicion_de_venta == CondicionDeVenta.CONTADO:
            canvas.drawString(503, 851, 'X')
            canvas.drawString(503, 528, 'X')
            canvas.drawString(503, 205, 'X')
        elif venta.condicion_de_venta == CondicionDeVenta.CREDITO:
            canvas.drawString(572, 851, 'X')
            canvas.drawString(572, 528, 'X')
            canvas.drawString(572, 205, 'X')

        if not venta.punto_de_entrega:
            canvas.drawString(130, 837, force_text(venta.cliente.razon_social or '').upper())
            canvas.drawString(130, 514, force_text(venta.cliente.razon_social or '').upper())
            canvas.drawString(130, 191, force_text(venta.cliente.razon_social or '').upper())
        else:
            cliente_y_direccion = f'{venta.cliente.razon_social}   DIRECCIÓN: {venta.punto_de_entrega.direccion}'
            canvas.drawString(130, 837, force_text(cliente_y_direccion or '').upper())
            canvas.drawString(130, 514, force_text(cliente_y_direccion or '').upper())
            canvas.drawString(130, 191, force_text(cliente_y_direccion or '').upper())
        canvas.drawString(51, 823, force_text(venta.cliente.ruc or ''))
        canvas.drawString(51, 500, force_text(venta.cliente.ruc or ''))
        canvas.drawString(51, 177, force_text(venta.cliente.ruc or ''))

        canvas.setFont("Helvetica", 10)
        detalles = DetalleDeVenta.objects.filter(venta=venta)
        total_venta = 0
        column_detail = 0
        if venta.iva == Iva.DIEZ:
            column_detail = 513
            canvas.drawString(252, 660, force_text(separar(math.ceil(venta.total / 11))).rjust(12, ' '))
            canvas.drawString(391, 660, force_text(separar(math.ceil(venta.total / 11))).rjust(12, ' '))
            canvas.drawString(252, 337, force_text(separar(math.ceil(venta.total / 11))).rjust(12, ' '))
            canvas.drawString(391, 337, force_text(separar(math.ceil(venta.total / 11))).rjust(12, ' '))
            canvas.drawString(252, 14, force_text(separar(math.ceil(venta.total / 11))).rjust(12, ' '))
            canvas.drawString(391, 14, force_text(separar(math.ceil(venta.total / 11))).rjust(12, ' '))
        elif venta.iva == Iva.CINCO:
            column_detail = 448
            canvas.drawString(142, 660, force_text(separar(math.ceil(venta.total / 21))).rjust(12, ' '))
            canvas.drawString(391, 660, force_text(separar(math.ceil(venta.total / 21))).rjust(12, ' '))
            canvas.drawString(142, 337, force_text(separar(math.ceil(venta.total / 21))).rjust(12, ' '))
            canvas.drawString(391, 337, force_text(separar(math.ceil(venta.total / 21))).rjust(12, ' '))
            canvas.drawString(142, 14, force_text(separar(math.ceil(venta.total / 21))).rjust(12, ' '))
            canvas.drawString(391, 14, force_text(separar(math.ceil(venta.total / 21))).rjust(12, ' '))
        elif venta.iva == Iva.EXENTA:
            column_detail = 383
            canvas.drawString(391, 660, force_text(0).rjust(12, ' '))
            canvas.drawString(391, 337, force_text(0).rjust(12, ' '))
            canvas.drawString(391, 14, force_text(0).rjust(12, ' '))

        row_sup = 800
        row_med = 477
        row_inf = 154
        for detalle in detalles:
            row_sup -= 15
            row_med -= 15
            row_inf -= 15
            canvas.drawString(91, row_sup, force_text(detalle.producto.descripcion))
            canvas.drawString(91, row_med, force_text(detalle.producto.descripcion))
            canvas.drawString(91, row_inf, force_text(detalle.producto.descripcion))
            canvas.drawString(292, row_sup, force_text(detalle.cantidad))
            canvas.drawString(292, row_med, force_text(detalle.cantidad))
            canvas.drawString(292, row_inf, force_text(detalle.cantidad))
            canvas.drawString(324, row_sup, force_text(separar(int(detalle.precio_unitario))).rjust(15, ' '))
            canvas.drawString(324, row_med, force_text(separar(int(detalle.precio_unitario))).rjust(15, ' '))
            canvas.drawString(324, row_inf, force_text(separar(int(detalle.precio_unitario))).rjust(15, ' '))
            canvas.drawString(column_detail, row_sup, force_text(separar(int(detalle.subtotal))).rjust(15, ' '))
            canvas.drawString(column_detail, row_med, force_text(separar(int(detalle.subtotal))).rjust(15, ' '))
            canvas.drawString(column_detail, row_inf, force_text(separar(int(detalle.subtotal))).rjust(15, ' '))
            total_venta += int(detalle.subtotal)

        canvas.setFont("Helvetica", 11)

        row_sup = 675
        row_med = 352
        row_inf = 29
        canvas.drawString(96, row_sup, numero_to_letras(int(venta.total)))
        canvas.drawString(96, row_med, numero_to_letras(int(venta.total)))
        canvas.drawString(96, row_inf, numero_to_letras(int(venta.total)))
        canvas.drawString(513, row_sup, force_text(separar(int(venta.total))).rjust(15, ' '))
        canvas.drawString(513, row_med, force_text(separar(int(venta.total))).rjust(15, ' '))
        canvas.drawString(513, row_inf, force_text(separar(int(venta.total))).rjust(15, ' '))

    venta = Venta.objects.get(pk=id)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % str(venta)

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    contenido(p, venta)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
