from django.conf.urls import url

from productos.ajax import get_producto

urlpatterns = [
    url('getproducto/$', get_producto),
]