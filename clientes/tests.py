from django.test import TestCase

from clientes.models import Cliente, PuntoEntregaCliente


class ClienteTest(TestCase):

    def crear_cliente(self, razon_social="Caño oxígeno"):
        return Cliente.objects.create(razon_social=razon_social)

    def test_cliente_creacion(self):
        c = self.crear_cliente()
        self.assertTrue(isinstance(c, Cliente))
        self.assertEqual(c.__str__(), f'{c.razon_social} (RUC: {c.ruc})')


class PuntoEntregaClienteTest(TestCase):

    def crear_punto(self, direccion="Avda. casi Calle 1234", referencia="Caño oxígeno"):
        cliente = Cliente.objects.create(razon_social="Cliente Prueba", ruc="80000000-0")
        return PuntoEntregaCliente.objects.create(cliente=cliente, direccion=direccion, referencia=referencia)

    def test_punto_creacion(self):
        p = self.crear_punto()
        self.assertTrue(isinstance(p, PuntoEntregaCliente))
        self.assertEqual(p.__str__(), f'{p.cliente.razon_social}: {p.direccion} ({p.referencia})')

