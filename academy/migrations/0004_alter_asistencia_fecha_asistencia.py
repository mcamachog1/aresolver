# Generated by Django 4.1.5 on 2023-01-28 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0003_asistencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='fecha_asistencia',
            field=models.DateField(),
        ),
    ]
