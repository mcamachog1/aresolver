from django.test import TestCase, Client
from django.db.models import Max
from .models import User, Alumno, Asistencia, Pago, Representante, Tutor, Asistencia
from datetime import datetime
from datetime import date
from .utils import *
from django.urls import reverse
from django.contrib.auth import authenticate,login
from .views import login_view

from pprint import pprint

# Create your tests here.

class AcademyTestCase(TestCase):
    def setUp(self):
        # Crear Usuario
        maryvi = User.objects.create_user(username="maryvi", email="mcamachog@gmail.com", password="12345")

        # Crear Academia
        academia = Academia.objects.create(nombre='AResolver', director=maryvi)
        # Crear alumnos
        # Alumno que si pago y si tiene asistencias
        alumno_1 = Alumno.objects.create(nombre="Pedrito", apellido="Lopez")
        alumno_1.academias.add(academia)
        # Alumno que no pago y no tiene asistencias
        alumno_2 = Alumno.objects.create(nombre="Laura", apellido="Perez")
        alumno_2.academias.add(academia)
        # Alumno que no pago y si tiene asistencias
        alumno_3 = Alumno.objects.create(nombre="Maria", apellido="Perez")
        alumno_3.academias.add(academia)
        # Alumno que si pago y no tiene asistencias
        alumno_4 = Alumno.objects.create(nombre="Cesar", apellido="Millan")
        alumno_4.academias.add(academia)

        # Crear pagos
        Pago.objects.create(fecha_pago=datetime.strptime("2023-02-16", "%Y-%m-%d"), monto=52, fecha_inicio=datetime.strptime("2023-02-16", "%Y-%m-%d"), total_clases=4, alumno=alumno_1, academia=academia)
        Pago.objects.create(fecha_pago=datetime.strptime("2023-02-16", "%Y-%m-%d"), monto=52, fecha_inicio=datetime.strptime("2023-02-16", "%Y-%m-%d"), total_clases=4, alumno=alumno_4, academia=academia)

        # Crear asistencias
        # Asistencias Alumno_1
        Asistencia.objects.create(fecha=datetime.strptime("2023-02-16", "%Y-%m-%d"),alumno=alumno_1, academia=academia)
        Asistencia.objects.create(fecha=datetime.strptime("2023-02-18", "%Y-%m-%d"),alumno=alumno_1, academia=academia)
        # Asistencias Alumno_3
        Asistencia.objects.create(fecha=datetime.strptime("2023-02-18", "%Y-%m-%d"),alumno=alumno_3, academia=academia)
        Asistencia.objects.create(fecha=datetime.strptime("2023-02-20", "%Y-%m-%d"),alumno=alumno_3, academia=academia)

    def test_usuario(self):
        usuario = User.objects.get(username='maryvi')
        self.assertEqual(usuario.username,'maryvi')
    
    def test_login(self):
        user = authenticate(username="maryvi", password="12345")
        self.assertEqual(user.username,'maryvi')
        self.assertEqual(user.academia.nombre, "AResolver")

    def test_pagos(self):
        alumno_1 = Alumno.objects.get(nombre='Pedrito')
        self.assertEqual(alumno_1.pagos_realizados.count(), 1)
        # datetime.strptime(date_str, '%m-%d-%Y').date()
        # self.assertEqual(ultimo_inicio_de_clases(alumno_1.id),datetime.strptime("2023-02-16", "%Y-%m-%d").date())
        # self.assertEqual(ultimo_inicio_de_clases(alumno_1.id),datetime.strptime("2023-02-16", "%Y-%m-%d").date())

    def test_pagos2(self):
        alumno_1 = Alumno.objects.get(nombre='Pedrito')
        # self.assertEqual(alumno_1.pagos_realizados.count(), 1)
        # datetime.strptime(date_str, '%m-%d-%Y').date()
        # self.assertEqual(ultimo_inicio_de_clases(alumno_1.id),datetime.strptime("2023-02-16", "%Y-%m-%d").date())
        self.assertEqual(ultimo_inicio_de_clases(alumno_1.id),datetime.strptime("2023-02-16", "%Y-%m-%d").date())

    def test_alumno_con_2_asistencias(self):
        alumno = Alumno.objects.get(nombre='Pedrito')
        c = Client()
        response = c.get(f"/alumno_entry/{alumno.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["porcentaje"], 50)

    def test_alumno_sin_asistencias(self):
        alumno = Alumno.objects.get(nombre='Laura')
        c = Client()
        response = c.get(f"/alumno_entry/{alumno.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["porcentaje"], 0)
    
    def test_alumno_con_asistencia_sin_pago(self):
        alumno = Alumno.objects.get(nombre='Maria')
        c = Client()
        response = c.get(f"/alumno_entry/{alumno.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["porcentaje"], 100)

    def test_alumnos(self):
        # user = login_view(email="mcamachog@gmail.com", password="12345")
        c = Client()
        c.login(email="mcamachog@gmail.com",password="12345")
        # response = c.post("/login", {"email":"mcamachog@gmail.com", "password": "12345"})
        # self.assertEqual(response.status_code, 200)
        response = c.get("/alumnos")
        self.assertEqual(response.status_code, 200)
        # print(len(response.context['alumnos']))
        # self.assertEqual(len(response.context["alumnos"]), 4)