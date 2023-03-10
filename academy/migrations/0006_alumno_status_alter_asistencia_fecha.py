# Generated by Django 4.1.5 on 2023-01-30 21:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0005_remove_asistencia_fecha_asistencia_asistencia_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='status',
            field=models.CharField(choices=[('N', 'Nuevo'), ('A', 'Activo'), ('I', 'Inactivo')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2023, 1, 30, 21, 0, 40, 184119)),
        ),
    ]
