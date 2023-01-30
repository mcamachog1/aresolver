from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse

from .models import User, Alumno, Asistencia

 # Create your views here.

def index(request):
    if request.method == 'POST':
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        nuevo = Alumno(nombre = nombre, apellido = apellido)
        nuevo.save()
        return HttpResponse(f"{nombre} {apellido}")
    # Listar los alumnos por orden de asistencia mas reciente
    # Crear estructura
    alumnos_fecha_mas_reciente = []
    # Seleccionar los alummnos
    alumnos = Alumno.objects.all()
    # Recorrer los alumnos y crear registro con alumno y fecha mas reciente de asistencia

    for alumno in alumnos:
        asistencia = Asistencia.objects.filter(alumno=alumno).order_by("-fecha").first()
        if True:
            fecha_str = "___ __-__-____"
        else:
            fecha_str = asistencia.fecha.strftime("%a %d-%m-%Y")
        registro = {"alumno": alumno, "fecha": fecha_str}
        alumnos_fecha_mas_reciente.append(registro)


    return render(request, "academy/index.html",{
        "asistencias": alumnos_fecha_mas_reciente
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