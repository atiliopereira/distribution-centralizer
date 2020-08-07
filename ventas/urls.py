from django.conf.urls import url

from ventas.views import anular_venta

urlpatterns = [
    url(r'^anular_venta/(?P<pk>\d+)/$', anular_venta, name='anular_venta'),
]