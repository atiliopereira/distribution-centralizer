# -*- coding: utf-8 -*-
import datetime
from dateutil import relativedelta

from django.db import models

from clientes.models import Cliente, PuntoEntregaCliente
from productos.models import Producto
from sistema.constants import EstadoDocumento
from sistema.models import Vehiculo, Ciudad, Funcionario, UnidadDeMedida, Local


class Remision(models.Model):
    class Meta:
        verbose_name = "Nota de remisión"
        verbose_name_plural = "Notas de remisión"

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

    punto_de_partida = models.ForeignKey(Local, on_delete=models.PROTECT, blank=True, null=True)
    direccion_del_punto_de_partida = models.CharField(max_length=200, blank=True, null=True)
    ciudad_de_partida = models.ForeignKey(Ciudad, blank=True, null=True, on_delete=models.PROTECT,
                                          related_name="ciudad_de_partida")
    departamento_de_partida = models.CharField(max_length=100, blank=True, null=True)

    punto_de_entrega = models.ForeignKey(PuntoEntregaCliente, on_delete=models.PROTECT, blank=True, null=True)
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

    def save(self, *args, **kwargs):
        if self.estado == EstadoDocumento.PENDIENTE:
            self.fecha_de_facturacion = self.get_fecha_de_facturacion()
        try:
            if self.punto_de_partida:
                if self.punto_de_partida.direccion:
                    self.direccion_del_punto_de_partida = self.punto_de_partida.direccion
                if self.punto_de_partida.ciudad:
                    self.ciudad_de_partida = self.punto_de_partida.ciudad
                if self.punto_de_partida.departamento:
                    self.departamento_de_partida = self.punto_de_partida.departamento.nombre

        except Exception as e:
            print(e)

        try:
            if self.punto_de_entrega:
                if self.punto_de_entrega.direccion:
                    self.direccion_del_punto_de_llegada = self.punto_de_entrega.direccion
                if self.punto_de_entrega.ciudad:
                    self.ciudad_de_llegada = self.punto_de_entrega.ciudad
                if self.punto_de_entrega.departamento:
                    self.departamento_de_llegada = self.punto_de_entrega.departamento.nombre
        except Exception as e:
            print(e)

        super(Remision, self).save(*args, **kwargs)

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
        return fecha_de_facturacion

    get_fecha_de_facturacion.short_description = 'Fecha de facturación'


class DetalleDeRemision(models.Model):
    class Meta:
        verbose_name = "Detalle de la remisión"
        verbose_name_plural = "Detalles de la remisión"

    remision = models.ForeignKey(Remision, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, blank=True, null=True, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Descripción detallada")
