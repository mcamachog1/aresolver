from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone
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
	def __str__(self):
		return (f"{self.email} {self.username}")


class Academia(models.Model):
	nombre = models.CharField(max_length=30)
	director = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		related_name="academia",
		null=True
	)
	url_imagen = models.URLField(max_length=200, null=True)

	def __str__(self):
		return self.nombre

# Clase Tutores
class Tutor(models.Model):
	nombre = models.CharField(max_length=30, blank=False)
	apellido = models.CharField(max_length=30)
	email = models.EmailField(max_length=254, null=True)
	fecha_nacimiento = models.DateTimeField(null=True)
	celular = models.CharField(max_length=15, null=True)
	academia = models.ForeignKey(Academia, on_delete=models.CASCADE, related_name="tutores", null=True)
	def serialize(self):
			return (f"{self.nombre} {self.apellido}")

# Clase Representantes
class Representante(models.Model):
	FEMENINO = 'F'
	MASCULINO = 'M'
	SEXO_CHOICES = [
			(FEMENINO, 'Femenino'),
			(MASCULINO, 'Masculino'),
	]	
	nombre = models.CharField(max_length=30, blank=False)
	apellido = models.CharField(max_length=30)
	email = models.EmailField(max_length=254, null=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_cambio = models.DateTimeField(auto_now=True)
	celular = models.CharField(max_length=15, null=True)
	sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True)
	academia = models.ForeignKey(Academia, on_delete=models.CASCADE, related_name="representantes", null=True)
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


class Pago(models.Model):
	fecha_pago = models.DateField()
	monto = models.DecimalField(max_digits=7, decimal_places=2)
	total_clases = models.DecimalField(max_digits=2, decimal_places=1)
	fecha_inicio = models.DateField()
	alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="pagos_realizados", null=False) 
	academia = models.ForeignKey(Academia, on_delete=models.CASCADE, related_name="pagos_realizados", null=True)

class Curso(models.Model):
	CONTINUO = 'C'
	FIJO = 'F'
	STATUS_CHOICES = [
			(CONTINUO, 'Continuo'),
			(FIJO, 'Fijo'),
	]
	nombre = models.CharField(max_length=50)
	costo_por_sesion = models.DecimalField(max_digits=4, decimal_places=2, null=True)
	tipo_de_curso = models.CharField(max_length=1, choices=STATUS_CHOICES, default=CONTINUO)
	cantidad_de_sesiones = models.PositiveSmallIntegerField(null=True)
	costo_curso_fijo = models.DecimalField(max_digits=4, decimal_places=2, null=True)
	tiempo_de_sesion = models.PositiveSmallIntegerField(null=True)

	def serialize(self):
		return (f" nombre: {self.nombre} - costo por sesion: {self.costo_por_sesion} - cantidad de sesiones: {self.cantidad_de_sesiones} - tipo de curso: {self.tipo_de_curso} - costo de curso fijo: {self.costo_curso_fijo}")

class Asistencia(models.Model):
	fecha = models.DateField(null=False, default=django.utils.timezone.now)
	alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="asistencias", null=False) 
	academia = models.ForeignKey(Academia, on_delete=models.CASCADE, related_name="asistencias", null=True)
	tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="asistencias", null=True)
	cantidad_sesiones = models.DecimalField(max_digits=2, decimal_places=1, default=1.0)
	curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="asistencias", null=True)

	def serialize(self):
		return (f"id: {self.id} fecha: {self.fecha} - alumno: {self.alumno.nombre} - academia: {self.academia.nombre} - tutor: {self.tutor.nombre}")
