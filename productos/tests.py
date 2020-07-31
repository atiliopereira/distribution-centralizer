from django.test import TestCase

from clientes.models import Cliente
from productos.models import Producto, ProductoCliente


class ProductoTest(TestCase):

    def crear_producto(self, descripcion="Caño oxígeno"):
        return Producto.objects.create(descripcion=descripcion)

    def test_producto_creacion(self):
        p = self.crear_producto()
        self.assertTrue(isinstance(p, Producto))
        self.assertEqual(p.__str__(), p.descripcion)


class ProductoClienteTest(TestCase):

    def crear_productocliente(self):
        cliente = Cliente.objects.create(razon_social="Cliente Prueba", ruc="80000000-0")
        producto = Producto.objects.create(descripcion="Caño oxígeno")
        return ProductoCliente.objects.create(cliente=cliente, producto=producto)

    def test_creacion_productocliente(self):
        pc = self.crear_productocliente()
        self.assertTrue(isinstance(pc, ProductoCliente))
        self.assertEqual(pc.__str__(), f'{pc.producto} ({pc.cliente}): {pc.precio}')
