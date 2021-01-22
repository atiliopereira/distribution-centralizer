from django.conf.urls import url

from administracion.views import DashboardView, VentasPorCliente, VentasChartView, RemisionesChartView

urlpatterns = [
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^ventasporcliente/$', VentasPorCliente.as_view(), name='ventasporcliente'),
    url(r'^remisioneschart/$', RemisionesChartView.as_view(), name='remisioneschart'),
    url(r'^ventaschart/$', VentasChartView.as_view(), name='ventaschart'),
]
