# Generated by Django 4.1.5 on 2023-04-01 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0041_alter_asistencia_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='cantidad_clases',
            field=models.DecimalField(decimal_places=1, default=1.0, max_digits=2),
        ),
    ]
