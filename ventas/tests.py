from django.test import TestCase

from clientes.models import Cliente
from ventas.models import Venta


class VentaTest(TestCase):

    def crear_venta(self, numero_de_factura='001-001-003226'):
        cliente = Cliente.objects.create(razon_social="Cliente Prueba", ruc="80000000-0")
        return Venta.objects.create(numero_de_factura=numero_de_factura, cliente=cliente)

    def test_creacion_venta(self):
        v = self.crear_venta()
        self.assertTrue(isinstance(v, Venta))
        self.assertEqual(v.__str__(),
                         f'Factura Venta {v.get_condicion_de_venta_display()} nro: {v.numero_de_factura} ({v.cliente})')
