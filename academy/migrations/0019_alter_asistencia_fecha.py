# Generated by Django 4.0.3 on 2023-02-15 11:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0018_alter_asistencia_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2023, 2, 15, 7, 45, 26, 741216)),
        ),
    ]