# Generated by Django 3.0.8 on 2020-07-31 22:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_auto_20200731_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='PuntoEntregaCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia', models.CharField(max_length=100, verbose_name='razón social')),
                ('direccion', models.CharField(blank=True, max_length=200, verbose_name='dirección')),
            ],
            options={
                'verbose_name': 'Punto de entrega',
                'verbose_name_plural': 'Puntos de entrega',
            },
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='grupo',
        ),
        migrations.AddField(
            model_name='cliente',
            name='dia_de_presentacion',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='día de presentación de facturas'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(blank=True, max_length=200, verbose_name='dirección de facturación'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='razon_social',
            field=models.CharField(max_length=150, verbose_name='razón social'),
        ),
        migrations.DeleteModel(
            name='Grupo',
        ),
        migrations.AddField(
            model_name='puntoentregacliente',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.Cliente'),
        ),
    ]
