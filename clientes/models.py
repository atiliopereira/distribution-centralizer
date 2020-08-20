# -*- coding: utf-8 -*-
from django.apps import apps
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from sistema.constants import EstadoDocumento
from sistema.models import Ciudad, Departamento


class Cliente(models.Model):
    razon_social = models.CharField(max_length=150, verbose_name="razón social")
    ruc = models.CharField(max_length=20, verbose_name="RUC", unique=True)
    direccion = models.CharField(max_length=200, blank=True, verbose_name="dirección de facturación")
    telefono = models.CharField(max_length=50, blank=True, verbose_name="teléfono")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="e-mail")
    dia_de_presentacion = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(30)],
                                              verbose_name="día de presentación de facturas")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.razon_social} (RUC: {self.ruc})'

    def get_deuda(self):
        facturas = apps.get_model("ventas", "Venta").objects.filter(cliente_id=self.id).filter(estado=EstadoDocumento.PENDIENTE)
        total = 0
        for factura in facturas:
            total += factura.total
        return total

    get_deuda.short_description = 'Deuda a la fecha'

    def get_remisiones_pendientes(self):
        remisiones = apps.get_model("remisiones", "remision").objects.filter(destino__cliente_id=self.id).filter(estado=EstadoDocumento.PENDIENTE)
        return remisiones.count()

    get_remisiones_pendientes.short_description = 'Remisiones pendientes de facturación'


class PuntoEntregaCliente(models.Model):
    class Meta:
        verbose_name = "Punto de entrega"
        verbose_name_plural = "Puntos de entrega"

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    referencia = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, verbose_name="dirección")
    ciudad = models.ForeignKey(Ciudad, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.cliente.razon_social}: {self.direccion} ({self.referencia})'
