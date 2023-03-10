# Generated by Django 4.1.5 on 2023-02-16 15:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0021_alter_asistencia_fecha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('fecha_nacimiento', models.DateTimeField(null=True)),
                ('celular', models.CharField(max_length=15, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2023, 2, 16, 15, 47, 19, 165072)),
        ),
    ]
