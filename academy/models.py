from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Alumno(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cohorte = models.PositiveSmallIntegerField(null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cambio = models.DateTimeField(auto_now=True)

# class Asistencia(models.Model):
#     fecha_asistencia = models.DateField(auto_now_add=True)
#     alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="asistencias", null=False) 