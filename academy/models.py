from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class User(AbstractUser):
	ALUMNO = 'A'
	REPRESENTANTE = 'R'
	DIRECTOR = 'D'
	TUTOR = 'T'
	VISITANTE = 'V'
	USER_TYPE_CHOICES = [
		(ALUMNO, 'Alumno'),
		(REPRESENTANTE, 'Representante'),
		(DIRECTOR, 'Director'),
		(TUTOR, 'Tutor'),
		(VISITANTE, 'Visitante')
	]
	tipo_de_usuario = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default=VISITANTE)


class Academia(models.Model):
	nombre = models.CharField(max_length=30)
	director = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		related_name="academia",
		null=True
	)

	def __str__(self):
		return self.nombre

# Clase Tutores
class Tutor(models.Model):
	nombre = models.CharField(max_length=30, blank=False)
	apellido = models.CharField(max_length=30)
	email = models.EmailField(max_length=254, null=True)
	fecha_nacimiento = models.DateTimeField(null=True)
	celular = models.CharField(max_length=15, null=True)
	academia = models.ForeignKey(Academia, on_delete=models.CASCADE, related_name="tutores_de_una_academia", null=True)
	def serialize(self):
			return (f"{self.nombre} {self.apellido}")

# Clase Representantes
class Representante(models.Model):
	nombre = models.CharField(max_length=30, blank=False)
	apellido = models.CharField(max_length=30)
	email = models.EmailField(max_length=254, null=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_cambio = models.DateTimeField(auto_now=True)
	celular = models.CharField(max_length=15, null=True)
	def serialize(self):
			return (f"{self.nombre} {self.apellido}")


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
	email = models.EmailField(max_length=254, null=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=NUEVO)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_cambio = models.DateTimeField(auto_now=True)
	representante = models.ForeignKey(Representante, on_delete=models.SET_NULL, related_name="representados", null=True)
	academias = models.ManyToManyField(Academia)

	class Meta:
		ordering = ['nombre']

	def __str__(self):
		return self.nombre

	def serialize(self):
		return (f"{self.nombre} {self.apellido} {self.representante.nombre}")


class Asistencia(models.Model):
	fecha = models.DateField(null=False, default=datetime.datetime.now())
	alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="asistencias", null=False) 
	academia = models.ForeignKey(Academia, on_delete=models.CASCADE, related_name="academias", null=True)
	tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="tutores", null=True)

	def serialize(self):
		return (f"id: {self.id} fecha: {self.fecha} - alumno: {self.alumno.nombre} - academia: {self.academia.nombre} - tutor: {self.tutor.nombre}")

class Pago(models.Model):
	fecha_pago = models.DateField()
	monto = models.DecimalField(max_digits=7, decimal_places=2)
	total_clases = models.IntegerField()
	fecha_inicio = models.DateField()
	alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="pagos_realizados", null=False) 
	academia = models.ForeignKey(Academia, on_delete=models.CASCADE, related_name="pagos_de_una_academia", null=True)