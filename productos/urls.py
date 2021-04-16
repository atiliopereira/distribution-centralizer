from django.conf.urls import url

from productos.ajax import get_producto
from productos.autocomplete import ProductoAutocomplete
from productos.views import ProductoDetailView

urlpatterns = [
    url('getproducto/$', get_producto),
    url(r'^producto_detail/(?P<pk>\d+)/$', ProductoDetailView.as_view(), name='producto_detail'),
    url(
        r'^productoautocomplete/$',
        ProductoAutocomplete.as_view(),
        name='producto-autocomplete',
    ),
]
