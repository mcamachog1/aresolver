from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class User(AbstractUser):
    pass

class Alumno(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cohorte = models.PositiveSmallIntegerField(null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cambio = models.DateTimeField(auto_now=True)

class Asistencia(models.Model):
    fecha_asistencia = models.DateField()
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="asistencias", null=False) 

    def __str__(self):
        return f"fecha: {self.fecha_asistencia} - alumno: {self.alumno.nombre}"