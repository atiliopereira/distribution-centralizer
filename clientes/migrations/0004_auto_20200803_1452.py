# Generated by Django 3.0.8 on 2020-08-03 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0003_auto_20200731_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puntoentregacliente',
            name='referencia',
            field=models.CharField(max_length=100),
        ),
    ]