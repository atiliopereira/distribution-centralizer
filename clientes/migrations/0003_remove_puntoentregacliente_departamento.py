# Generated by Django 3.0.8 on 2020-08-20 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_auto_20200820_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puntoentregacliente',
            name='departamento',
        ),
    ]
