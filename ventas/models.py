# -*- coding: utf-8 -*-
import datetime

from django.db import models

from clientes.models import Cliente
from remisiones.models import Remision, DetalleDeRemision
from ventas.constants import CondicionDeVenta, Iva
from productos.models import Producto, ProductoCliente, get_precio
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
        return f'Factura Venta {self.get_condicion_de_venta_display()} nro: {self.numero_de_factura} ({self.cliente})'

    def get_total(self):
        detalles = DetalleDeVenta.objects.filter(venta=self)
        suma = 0
        for detalle in detalles:
            suma += detalle.subtotal
        return suma

    def save(self, *args, **kwargs):
        self.total = self.get_total()
        super(Venta, self).save(*args, **kwargs)


class DetalleDeVenta(models.Model):
    class Meta:
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de venta"

    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Descripción")
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0)


class RemisionEnVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    remision = models.ForeignKey(Remision, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.remision.estado = EstadoDocumento.CONFIRMADO
        self.remision.save()
        detalles = DetalleDeRemision.objects.filter(remision=self.remision)
        for detalle in detalles:
            precio = get_precio(self.venta.cliente, detalle.producto, detalle.remision.fecha_de_emision)
            subtotal = precio * detalle.cantidad
            DetalleDeVenta.objects.create(venta=self.venta, cantidad=detalle.cantidad, producto=detalle.producto,
                                          precio_unitario=precio, subtotal=subtotal)
            self.venta.save()
        super(RemisionEnVenta, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.remision.estado = EstadoDocumento.PENDIENTE
        self.remision.save()
        super(RemisionEnVenta, self).delete(*args, **kwargs)