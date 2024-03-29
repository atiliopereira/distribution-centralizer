# Generated by Django 3.0.8 on 2020-08-21 00:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripción del cargo')),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Ciudades',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Departamentos',
            },
        ),
        migrations.CreateModel(
            name='UnidadDeMedida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('simbolo', models.CharField(blank=True, max_length=10, null=True, verbose_name='Símbolo')),
            ],
            options={
                'verbose_name': 'unidad de medida',
                'verbose_name_plural': 'unidades de medida',
            },
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=100)),
                ('rua', models.CharField(max_length=100, verbose_name='número de registro único del automotor')),
                ('rua_remolque', models.CharField(blank=True, max_length=100, null=True, verbose_name='número de registro único del automotor de remolquetracto o semiremolque')),
            ],
            options={
                'verbose_name': 'Vehículo',
                'verbose_name_plural': 'Vehículos',
            },
        ),
        migrations.CreateModel(
            name='Local',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia', models.CharField(max_length=100)),
                ('direccion', models.CharField(blank=True, max_length=200, verbose_name='dirección')),
                ('ciudad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sistema.Ciudad')),
            ],
            options={
                'verbose_name': 'Local',
                'verbose_name_plural': 'Locales',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Nombre y apellido', max_length=250)),
                ('ruc', models.CharField(blank=True, max_length=20, null=True, verbose_name='RUC/CI Nro.')),
                ('direccion', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('fecha_de_ingreso', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('observaciones', models.TextField(blank=True, max_length=500, null=True)),
                ('cargo', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='sistema.Cargo')),
                ('usuario', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ciudad',
            name='departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sistema.Departamento'),
        ),
    ]
