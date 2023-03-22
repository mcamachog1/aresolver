# Generated by Django 4.1.5 on 2023-03-03 18:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0032_pago_academia_alter_asistencia_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='academia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutores_de_una_academia', to='academy.academia'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2023, 3, 3, 18, 47, 39, 951963)),
        ),
    ]