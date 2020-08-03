from django.test import TestCase

from clientes.models import Cliente
from remisiones.models import Remision


class RemisionTest(TestCase):

    def crear_remision(self, numero_de_remision='001-001-0001740'):
        cliente = Cliente.objects.create(razon_social="Cliente Prueba", ruc="80000000-0")
        return Remision.objects.create(numero_de_remision=numero_de_remision, cliente=cliente)

    def test_creacion_remision(self):
        r = self.crear_remision()
        self.assertTrue(isinstance(r, Remision))
        self.assertEqual(r.__str__(), f'Remisión Nro: {r.numero_de_remision}')
