# Generated by Django 4.0.3 on 2023-02-03 11:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0007_alter_asistencia_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2023, 2, 3, 7, 50, 57, 556855)),
        ),
    ]
