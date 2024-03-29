from django.conf.urls import url

from remisiones.reports import lista_remisiones
from remisiones.views import RemisionDetailView, anular_remision

urlpatterns = [
    url(r'^remision_detail/(?P<pk>\d+)/$', RemisionDetailView.as_view(), name='remision_detail'),
    url(r'^anular_remision/(?P<pk>\d+)/$', anular_remision, name='anular_remision'),
    url(r'^lista_remisiones/$', lista_remisiones, name='lista_remisiones'),
]