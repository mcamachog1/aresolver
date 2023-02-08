from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class User(AbstractUser):
    pass

class Alumno(models.Model):
	NUEVO = 'N'
	ACTIVO = 'A'
	INACTIVO = 'I'
	STATUS_CHOICES = [
			(NUEVO, 'Nuevo'),
			(ACTIVO, 'Activo'),
			(INACTIVO, 'Inactivo'),
	]
	nombre = models.CharField(max_length=30)
	apellido = models.CharField(max_length=30)
	cohorte = models.PositiveSmallIntegerField(null=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=NUEVO)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_cambio = models.DateTimeField(auto_now=True)

	def serialize(self):
			return (f"{self.nombre} {self.apellido} {self.status}")

class Asistencia(models.Model):
    fecha = models.DateField(null=False, default=datetime.datetime.now())
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="asistencias", null=False) 

    def serialize(self):
        return (f"id: {self.id} fecha: {self.fecha} - alumno: {self.alumno.nombre}")

class Pago(models.Model):
	fecha_pago = models.DateTimeField(auto_now_add=True)
	monto = models.DecimalField(max_digits=7, decimal_places=2)
	total_clases = models.IntegerField()
	fecha_inicio = models.DateTimeField(auto_now_add=True)
	alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="pagos_realizados", null=False) 