# Generated by Django 4.1.5 on 2023-04-01 15:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0040_alter_asistencia_fecha_alter_pago_total_clases'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]