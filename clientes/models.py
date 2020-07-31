# -*- coding: utf-8 -*-
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    dia_de_presentacion = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(30)],
                                              verbose_name="día de presentación de facturas")

    def __repr__(self):
        return f'Grupo({self.nombre}, {self.dia_de_presentacion})'

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    grupo = models.ForeignKey(Grupo, null=True, blank=True, on_delete=models.PROTECT)
    razon_social = models.CharField(max_length=100, verbose_name="razón social")
    ruc = models.CharField(max_length=20, verbose_name="RUC", unique=True)
    direccion = models.CharField(max_length=200, blank=True, verbose_name="dirección")
    telefono = models.CharField(max_length=50, blank=True, verbose_name="teléfono")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="e-mail")
    activo = models.BooleanField(default=True)

    def __repr__(self):
        return f'Cliente({self.razon_social}, {self.ruc}, {self.direccion}, {self.telefono}, {self.email}, ' \
               f'{self.email}, {self.activo}'

    def __str__(self):
        return self.razon_social

