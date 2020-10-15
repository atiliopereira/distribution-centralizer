# -*- coding: utf-8 -*-
import datetime

from django.db import models

from clientes.models import Cliente, PuntoEntregaCliente
from remisiones.models import Remision, DetalleDeRemision
from sistema.models import Vehiculo
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
    punto_de_entrega = models.ForeignKey(PuntoEntregaCliente, null=True, blank=True,
                                  verbose_name="Dirección del punto de entrega", on_delete=models.PROTECT, editable=False)
    vehiculo = models.ForeignKey(Vehiculo, null=True, blank=True, on_delete=models.PROTECT)
    iva = models.CharField(max_length=2, choices=Iva.PORCENTAJES, default=Iva.DIEZ)
    estado = models.CharField(max_length=3, choices=EstadoDocumento.ESTADOS,
                              default=EstadoDocumento.PENDIENTE, editable=False)
    total = models.DecimalField(max_digits=15, decimal_places=0, default=0)

    def __str__(self):
        return f'Factura Venta {self.get_condicion_de_venta_display()} nro: {self.numero_de_factura} ({self.cliente})'

    def get_total(self):
        detalles = DetalleDeVenta.objects.filter(venta=self)
        suma = 0
        for detalle in detalles:
            suma += detalle.subtotal
        return suma

    @property
    def tiene_remisiones(self):
        remisiones_en_venta = RemisionEnVenta.objects.filter(venta=self).count()
        return remisiones_en_venta

    def get_direccion(self):
        direccion = ''
        if self.punto_de_entrega:
            direccion = f'{self.punto_de_entrega.direccion} ({self.punto_de_entrega.referencia})'
        return direccion
    get_direccion.short_description = 'Dirección'

    def save(self, *args, **kwargs):
        if self.pk:
            self.total = self.get_total()
        if self.condicion_de_venta == CondicionDeVenta.CONTADO and not self.pk:
            self.estado = EstadoDocumento.CONFIRMADO
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
        detalles_de_remision = DetalleDeRemision.objects.filter(remision=self.remision)

        for detalle_de_remision in detalles_de_remision:
            if DetalleDeVenta.objects.filter(venta=self.venta).filter(producto=detalle_de_remision.producto).exists():
                detalle_de_venta = DetalleDeVenta.objects.filter(venta=self.venta).get(
                    producto=detalle_de_remision.producto)
                detalle_de_venta.cantidad += detalle_de_remision.cantidad
                detalle_de_venta.subtotal = detalle_de_venta.cantidad * detalle_de_venta.precio_unitario
                detalle_de_venta.save()
            else:
                precio = get_precio(self.venta.cliente, detalle_de_remision.producto,
                                    detalle_de_remision.remision.fecha_de_emision)
                subtotal = precio * detalle_de_remision.cantidad
                DetalleDeVenta.objects.create(venta=self.venta, cantidad=detalle_de_remision.cantidad,
                                              producto=detalle_de_remision.producto, precio_unitario=precio,
                                              subtotal=subtotal)
        self.remision.estado = EstadoDocumento.CONFIRMADO
        self.remision.save()
        self.venta.save()
        super(RemisionEnVenta, self).save(*args, **kwargs)
