# Generated by Django 4.0.3 on 2023-01-30 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0004_alter_asistencia_fecha_asistencia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asistencia',
            name='fecha_asistencia',
        ),
        migrations.AddField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(null=True),
        ),
    ]
