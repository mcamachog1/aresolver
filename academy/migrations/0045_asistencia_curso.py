# Generated by Django 4.1.5 on 2023-04-05 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0044_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='curso',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asistencias', to='academy.curso'),
        ),
    ]
