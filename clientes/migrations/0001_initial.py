# Generated by Django 3.0.8 on 2020-07-31 18:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('dia_de_presentacion', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='día de presentación de facturas')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon_social', models.CharField(max_length=100, verbose_name='razón social')),
                ('ruc', models.CharField(max_length=20, unique=True, verbose_name='RUC')),
                ('direccion', models.CharField(blank=True, max_length=200, verbose_name='dirección')),
                ('telefono', models.CharField(blank=True, max_length=50, verbose_name='teléfono')),
                ('email', models.CharField(blank=True, max_length=100, null=True, verbose_name='e-mail')),
                ('activo', models.BooleanField(default=True)),
                ('grupo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='clientes.Grupo')),
            ],
        ),
    ]
