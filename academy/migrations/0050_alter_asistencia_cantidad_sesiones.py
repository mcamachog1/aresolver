# Generated by Django 4.1.5 on 2023-04-27 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0049_alter_pago_total_clases'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='cantidad_sesiones',
            field=models.IntegerField(),
        ),
    ]