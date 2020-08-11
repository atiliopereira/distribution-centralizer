# Generated by Django 3.0.8 on 2020-07-31 19:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0002_auto_20200731_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=150, verbose_name='descripción')),
                ('precio', models.DecimalField(decimal_places=0, default=0, max_digits=15)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=0, default=0, max_digits=15)),
                ('fecha_de_creacion', models.DateTimeField(default=datetime.date.today, editable=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.Cliente')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='productos.Producto')),
            ],
        ),
    ]