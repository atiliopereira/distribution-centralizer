from django.conf.urls import url

from remisiones.views import RemisionDetailView

urlpatterns = [
    url(r'^remision_detail/(?P<pk>\d+)/$', RemisionDetailView.as_view(), name='remision_detail'),
]