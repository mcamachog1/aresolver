# Generated by Django 4.1.5 on 2023-04-05 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0045_asistencia_curso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='costo_por_sesion',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
    ]
