# Generated by Django 4.1.5 on 2023-03-10 21:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0035_alter_asistencia_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2023, 3, 10, 21, 8, 18, 79831)),
        ),
    ]
