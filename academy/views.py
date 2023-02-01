from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
# from datetime import datetime

from django.http import JsonResponse

from .models import User, Alumno, Asistencia

 # Create your views here.

def crear_alumno(nombre, apellido):
    nuevo = Alumno(nombre = nombre, apellido = apellido)
    nuevo.save()

# Listar los alumnos por orden de asistencia mas reciente
def listar_alumnos_por_fecha_de_asistencia():
    # Crear estructura
    alumnos_fecha_mas_reciente = []
    # Seleccionar los alummnos
    alumnos = Alumno.objects.all()
    # Recorrer los alumnos y crear registro con alumno y fecha mas reciente de asistencia
    for alumno in alumnos:
        asistencia = Asistencia.objects.filter(alumno=alumno).order_by("-fecha").first()
        if asistencia is not None:
            fecha_str = asistencia.fecha.strftime("%a %d-%m-%Y")
        else:
            fecha_str = alumno.fecha_creacion.strftime("%a %d-%m-%Y")
        registro = {"nombre": f"{alumno.nombre} {alumno.apellido}", "fecha": fecha_str, "status": alumno.get_status_display()}
        alumnos_fecha_mas_reciente.append(registro)
    return (alumnos_fecha_mas_reciente)


def index(request):
    if request.method == 'POST':
        crear_alumno(request.POST["nombre"],request.POST["apellido"])
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "academy/index.html",{
            "alumnos": listar_alumnos_por_fecha_de_asistencia(),
            })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "academy/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "academy/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register_view(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "academy/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "academy/register.html", {
                "message": "Email address already taken."
            })
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "academy/register.html")