import datetime

from django.db.models import Sum
from django.views.generic import TemplateView, ListView

from remisiones.models import Remision
from sistema.constants import EstadoDocumento
from sistema.globales import mes_anho_en_letras, random_colors
from ventas.models import Venta


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


class VentasPorCliente(ListView):
    model = Venta
    template_name = "ventas_por_cliente.html"

    def get_queryset(self):
        ventas = Venta.objects.filter(estado=EstadoDocumento.CONFIRMADO)
        fecha_desde = self.request.GET.get('fecha_desde', '')
        if fecha_desde != '':
            ventas = ventas.filter(fecha_de_emision__gte=fecha_desde)

        fecha_hasta = self.request.GET.get('fecha_hasta', '')
        if fecha_hasta != '':
            ventas = ventas.filter(fecha_de_emision__lte=fecha_hasta)

        clientes = [[venta.cliente, ventas.filter(cliente_id=venta.cliente.id).count(),
                     ventas.filter(cliente_id=venta.cliente.id).aggregate(total=Sum('total')).get('total')] for venta in
                    ventas.distinct('cliente') if
                    ventas.filter(cliente_id=venta.cliente.id).aggregate(total=Sum('total')).get('total')]

        return sorted(clientes, key=lambda t: t[2], reverse=True)

    def get_context_data(self, **kwargs):
        context = super(VentasPorCliente, self).get_context_data(**kwargs)
        context['fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        return context


class RemisionesChartView(ListView):
    model = Remision
    template_name = 'remision_chart.html'

    def get_queryset(self):
        remisiones = Remision.objects.exclude(estado=EstadoDocumento.ANULADO)
        fecha_desde = self.request.GET.get('fecha_desde', '')
        if fecha_desde != '':
            remisiones = remisiones.filter(fecha_de_emision__gte=fecha_desde)

        fecha_hasta = self.request.GET.get('fecha_hasta', '')
        if fecha_hasta != '':
            remisiones = remisiones.filter(fecha_de_emision__lte=fecha_hasta)

        result = [[remision.vehiculo, remisiones.filter(vehiculo=remision.vehiculo).count()] for
                     remision in remisiones.distinct('vehiculo') if
                     remisiones.filter(vehiculo=remision.vehiculo).count() > 0]
        return sorted(result, key=lambda s: s[1], reverse=True)

    def get_context_data(self, **kwargs):
        context = super(RemisionesChartView, self).get_context_data(**kwargs)
        context['colores'] = random_colors(len(self.get_queryset()))
        context['fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        return context


class VentasChartView(TemplateView):
    template_name = 'ventas_anuales.html'

    def get_context_data(self, **kwargs):
        context = super(VentasChartView, self).get_context_data(**kwargs)
        mes_actual = datetime.date.today().month
        anho_actual = datetime.date.today().year
        meses = [[mes_actual, anho_actual]]
        total_ventas = [int(get_total_ventas_mes(mes_actual, anho_actual)/1000)]
        for i in range(11):
            mes_actual = mes_actual - 1
            if mes_actual < 1:
                mes_actual = 12
                anho_actual -= 1
            meses.append([mes_actual, anho_actual])
            total_ventas.append(int(get_total_ventas_mes(mes_actual, anho_actual)/1000))
        context['meses'] = [mes_anho_en_letras(*mes) for mes in meses][::-1]
        context['total_ventas'] = total_ventas[::-1]
        return context


def get_total_ventas_mes(mes, anho):
    return Venta.objects.filter(fecha_de_emision__year=anho).filter(fecha_de_emision__month=mes).exclude(
        estado=EstadoDocumento.ANULADO).aggregate(total=Sum('total')).get('total') or 0
