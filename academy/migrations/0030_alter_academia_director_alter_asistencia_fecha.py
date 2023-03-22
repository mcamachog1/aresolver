# Generated by Django 4.1.5 on 2023-03-03 13:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0029_user_tipo_de_usuario_alter_asistencia_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academia',
            name='director',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='academia', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2023, 3, 3, 13, 22, 0, 245795)),
        ),
    ]