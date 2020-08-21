# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models


class Departamento(models.Model):
    class Meta:
        verbose_name_plural = "Departamentos"
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre}'


class Ciudad(models.Model):
    class Meta:
        verbose_name_plural = "Ciudades"
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.nombre}'


class Vehiculo(models.Model):
    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"

    marca = models.CharField(max_length=100)
    rua = models.CharField(max_length=100, verbose_name="número de registro único del automotor")
    rua_remolque = models.CharField(max_length=100, blank=True, null=True,
                                    verbose_name="número de registro único del automotor de remolquetracto o semiremolque")

    def __str__(self):
        return f'{self.marca} ({self.rua})'


class Cargo(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name='Descripción del cargo')

    def __str__(self):
        return f'{self.descripcion}'


class Funcionario(models.Model):
    nombre = models.CharField(max_length=250, help_text="Nombre y apellido")
    cargo = models.ForeignKey(Cargo, blank=True, on_delete=models.PROTECT)
    ruc = models.CharField(max_length=20, verbose_name="RUC/CI Nro.", null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    fecha_de_ingreso = models.DateField(default=datetime.date.today, null=True, blank=True)
    observaciones = models.TextField(max_length=500, null=True, blank=True)
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        if self.cargo:
            return f'{self.nombre} ({self.cargo})'
        else:
            return f'{self.nombre} (Cargo no especificado)'


class UnidadDeMedida(models.Model):
    class Meta:
        verbose_name = "unidad de medida"
        verbose_name_plural = "unidades de medida"

    nombre = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=10, blank=True, null=True, verbose_name="Símbolo")

    def __str__(self):
        return f'{self.nombre} ({self.simbolo})'


class Local(models.Model):
    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locales"

    referencia = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, verbose_name="dirección")
    ciudad = models.ForeignKey(Ciudad, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.referencia}'
