# Generated by Django 4.0.3 on 2023-02-09 11:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0013_representante_alter_asistencia_fecha_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='representante',
            name='celular',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2023, 2, 9, 7, 57, 51, 954652)),
        ),
    ]
