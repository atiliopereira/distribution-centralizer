# -*- coding: utf-8 -*-
import datetime

from django.db import models

from clientes.models import Cliente


class Producto(models.Model):
    descripcion = models.CharField(max_length=150, verbose_name="descripción")
    precio = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


class ProductoCliente(models.Model):
    class Meta:
        verbose_name = "Producto por cliente"
        verbose_name_plural = 'Productos por cliente'
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    fecha_de_creacion = models.DateField(default=datetime.date.today, editable=False)

    def __str__(self):
        return f'{self.producto} ({self.cliente}): {self.precio}'


