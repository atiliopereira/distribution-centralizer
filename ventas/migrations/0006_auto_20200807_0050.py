# Generated by Django 3.0.8 on 2020-08-07 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_auto_20200806_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalledeventa',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.Venta'),
        ),
    ]
