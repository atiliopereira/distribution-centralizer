import datetime

from django.db import models

from clientes.models import Cliente
from ventas.constants import CondicionDeVenta, Iva
from productos.models import Producto
from sistema.constants import EstadoDocumento


class Venta(models.Model):
    class Meta:
        verbose_name = "Factura de venta"
        verbose_name_plural = "Facturas de venta"
    numero_de_factura = models.CharField(max_length=30)
    fecha_de_emision = models.DateField(default=datetime.date.today)
    condicion_de_venta = models.CharField(max_length=3, choices=CondicionDeVenta.CONDICIONES,
                                          default=CondicionDeVenta.CONTADO, verbose_name='Condición de venta')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    iva = models.CharField(max_length=2, choices=Iva.PORCENTAJES, default=Iva.DIEZ)
    estado = models.CharField(max_length=3, choices=EstadoDocumento.ESTADOS,
                              default=EstadoDocumento.PENDIENTE, editable=False)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f'Factura Venta {self.condicion_de_venta} nro: {self.numero_de_factura} ({self.cliente})'


class DetalleDeVenta(models.Model):
    class Meta:
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de venta"

    venta = models.ForeignKey(Venta, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Descripción")
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0)