from django.test import TestCase, Client
from django.db.models import Max
from .models import User, Alumno, Asistencia, Pago, Representante, Tutor
from datetime import datetime

# Create your tests here.

class AcademyTestCase(TestCase):
    def setUp(self):
        # Crear alumnos
        alumno_1 = Alumno.objects.create(nombre="Pedrito", apellido="Lopez")
        alumno_2 = Alumno.objects.create(nombre="Laura", apellido="Perez")
        
        # Crear pagos
        pago_1 = Pago.objects.create(fecha_pago=datetime.strptime("2023-02-16", "Y-m-d"), monto=52, fecha_inicio=datetime.strptime("2023-02-16", "Y-m-d"), total_clases=4, alumno=alumno_1)
        