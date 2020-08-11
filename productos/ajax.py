import datetime

from django.http.response import JsonResponse

from clientes.models import Cliente
from productos.models import Producto, get_precio


def get_producto(request):
    producto_id = (request.GET['producto_id']).replace(" ", "")
    cliente_id = (request.GET['cliente_id']).replace(" ", "")
    datos = {}
    cliente = Cliente.objects.get(id=cliente_id)
    producto = Producto.objects.get(id=producto_id)
    fecha = datetime.date.today()

    precio = get_precio(cliente=cliente, producto=producto, fecha=fecha)

    datos.update({'precio': int(precio)})

    return JsonResponse(datos)
