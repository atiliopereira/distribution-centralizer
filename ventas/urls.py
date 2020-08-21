from django.conf.urls import url

from ventas.reports import lista_ventas
from ventas.views import anular_venta, VentaDetailView, confirmar_venta

urlpatterns = [
    url(r'^venta_detail/(?P<pk>\d+)/$', VentaDetailView.as_view(), name='venta_detail'),
    url(r'^anular_venta/(?P<pk>\d+)/$', anular_venta, name='anular_venta'),
    url(r'^confirmar_venta/(?P<pk>\d+)/$', confirmar_venta, name='confirmar_venta'),
    url(r'^lista_ventas/$', lista_ventas, name='lista_ventas'),
]
