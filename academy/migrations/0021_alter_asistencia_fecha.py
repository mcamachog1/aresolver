# Generated by Django 4.1.5 on 2023-02-15 13:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0020_alter_alumno_representante_alter_asistencia_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2023, 2, 15, 13, 19, 10, 972658)),
        ),
    ]
