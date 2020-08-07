from django.shortcuts import render, redirect
from django.template import RequestContext

from sistema.constants import EstadoDocumento
from ventas.models import Venta, RemisionEnVenta


def anular_venta(request, pk):
    context = RequestContext(request)
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
    return render(request, 'venta_confirm.html', {'mensaje': mensaje, 'advertencia': advertencia})
