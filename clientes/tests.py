from django.test import TestCase

from clientes.models import Cliente, Grupo


class GrupoTest(TestCase):

    def crear_grupo(self, nombre="Caño oxígeno"):
        return Grupo.objects.create(nombre=nombre)

    def test_grupo_creacion(self):
        g = self.crear_grupo()
        self.assertTrue(isinstance(g, Grupo))
        self.assertEqual(g.__str__(), g.nombre)


class ClienteTest(TestCase):

    def crear_cliente(self, razon_social="Caño oxígeno"):
        return Cliente.objects.create(razon_social=razon_social)

    def test_cliente_creacion(self):
        c = self.crear_cliente()
        self.assertTrue(isinstance(c, Cliente))
        self.assertEqual(c.__str__(), c.razon_social)