# -*- coding: utf-8 -*-
import datetime
from dateutil import relativedelta

from django.db import models

from clientes.models import Cliente
from productos.models import Producto
from sistema.constants import EstadoDocumento
from sistema.models import Vehiculo, Ciudad, Funcionario, UnidadDeMedida


class Remision(models.Model):
    class Meta:
        verbose_name = "Remisión"
        verbose_name_plural = "Remisiones"

    # datos de la remision
    numero_de_remision = models.CharField(max_length=30)
    fecha_de_emision = models.DateField(default=datetime.date.today)

    # destinatario de la mercaderia
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)

    # datos del traslado
    motivo_del_traslado = models.CharField(max_length=100, blank=True, null=True)
    comprobante_de_venta = models.CharField(max_length=100, blank=True, null=True)
    numero_de_comprobante_de_venta = models.CharField(max_length=100, blank=True, null=True)
    numero_de_timbrado = models.CharField(max_length=100, blank=True, null=True)
    fecha_de_expedicion = models.DateField(default=datetime.date.today, blank=True, null=True)

    fecha_de_inicio_del_traslado = models.DateField(default=datetime.date.today, blank=True, null=True)
    fecha_estimada_de_termino_del_traslado = models.DateField(default=datetime.date.today, blank=True, null=True)

    direccion_del_punto_de_partida = models.CharField(max_length=200, blank=True, null=True)
    ciudad_de_partida = models.ForeignKey(Ciudad, blank=True, null=True, on_delete=models.PROTECT,
                                          related_name="ciudad_de_partida")
    departamento_de_partida = models.CharField(max_length=100, blank=True, null=True)

    direccion_del_punto_de_llegada = models.CharField(max_length=200, blank=True, null=True)
    ciudad_de_llegada = models.ForeignKey(Ciudad, blank=True, null=True, on_delete=models.PROTECT,
                                          related_name='ciudad_de_llegada')
    departamento_de_llegada = models.CharField(max_length=100, blank=True, null=True)

    kilometros_estimados_de_recorrido = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    cambio_de_fecha_de_termino_del_traslado_o_punto_de_llegada = models.CharField(max_length=100, blank=True, null=True)
    motivo = models.CharField(max_length=100, blank=True, null=True)

    # datos del vehiculo de transporte
    vehiculo = models.ForeignKey(Vehiculo, null=True, blank=True, on_delete=models.PROTECT)

    # datos del conductor del vehiculo
    chofer = models.ForeignKey(Funcionario, null=True, blank=True, on_delete=models.PROTECT)

    estado = models.CharField(max_length=3, choices=EstadoDocumento.ESTADOS,
                              default=EstadoDocumento.PENDIENTE, editable=False)
    fecha_de_facturacion = models.DateField(null=True, blank=True, editable=False)

    def __str__(self):
        return f'Remisión Nro: {self.numero_de_remision}'

    def get_fecha_de_facturacion(self):
        hoy = datetime.date.today()
        fecha_vencimiento_mes_actual = datetime.datetime(hoy.year, hoy.month, self.cliente.dia_de_presentacion)
        fecha_de_facturacion = fecha_vencimiento_mes_actual
        if not self.fecha_de_facturacion:
            if int(hoy.day) <= int(self.cliente.dia_de_presentacion):
                pass
            elif int(hoy.day) > int(self.cliente.dia_de_presentacion):
                nextmonth = datetime.date.today() + relativedelta.relativedelta(months=1)
                fecha_de_facturacion = datetime.datetime(nextmonth.year, nextmonth.month, self.cliente.dia_de_presentacion)
        else:
            fecha_de_facturacion = self.fecha_de_facturacion
        return fecha_de_facturacion.date()

    get_fecha_de_facturacion.short_description = 'Fecha de facturación'


class DetalleDeRemision(models.Model):
    class Meta:
        verbose_name = "Detalle de la remisión"
        verbose_name_plural = "Detalles de la remisión"

    remision = models.ForeignKey(Remision, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, blank=True, null=True, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Descripción detallada")
