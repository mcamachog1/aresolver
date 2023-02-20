from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from .models import User, Alumno, Asistencia, Pago, Representante, Tutor
from .utils import *

# Alumnos

# Listar los alumnos
def alumnos(request):
    return render(request, "academy/alumnos.html", {
        "alumnos": listar_alumnos_por_fecha_de_asistencia(),        
    })  

# Crear un nuevo alumno
def alumno_new(request):
    if (request.method == 'POST'):
        alumno = Alumno()
        alumno.nombre = request.POST['nombre']
        alumno.apellido = request.POST['apellido']
        alumno.save()
        return HttpResponseRedirect(reverse("alumnos"))    

# Eliminar un alumno 
def alumno_delete(request, alumno_id):
    alumno = Representante.objects.get(id=alumno_id)
    alumno.delete()
    return HttpResponseRedirect(reverse("alumnos"))   

# Ver un alumno
def alumno_entry(request, alumno_id):
    return render(request, "academy/alumnos.html", {
        "alumno": Alumno.objects.get(id=alumno_id),
    })  

# Editar un alumno
def alumno_edit(request, alumno_id):
    sin_representante = False
    if request.method == 'GET':
        ultimo_pago = Pago.objects.filter(alumno=Alumno.objects.get(id=alumno_id)).order_by('-fecha_pago').first()
        # ultimo_pago.fecha_inicio
        mi_representante = Alumno.objects.get(id=alumno_id).representante
        if mi_representante is None :
            sin_representante = True
        return render(request, "academy/perfil.html", {
            "alumno": Alumno.objects.get(id=alumno_id),
            "representantes": Representante.objects.all(),
            "pagos": Pago.objects.filter(alumno=Alumno.objects.get(id=alumno_id)).order_by('-fecha_pago'),
            "sin_representante": sin_representante,
            "clases_vistas": "clases_vistas"
        })
    elif (request.method == 'POST'):
        perfil = {"id": alumno_id,
                  "nombre": request.POST["nombre"],
                  "apellido": request.POST["apellido"]}
        # print (perfil)
        actualizar_perfil(perfil)
        return HttpResponseRedirect(reverse("alumnos"))


# Representantes

# Listar los representantes
def representantes(request):
    return render(request, "academy/representantes.html", {
        "representantes": Representante.objects.all(),
    })  

# Crear un nuevo representante
def representante_new(request):
    if (request.method == 'POST'):
        representante = Representante()
        representante.nombre = request.POST['nombre']
        representante.apellido = request.POST['apellido']
        representante.save()
        return HttpResponseRedirect(reverse("representantes"))    

# Eliminar un representante    
def representante_delete(request, representante_id):
    representante = Representante.objects.get(id=representante_id)
    representante.delete()
    return HttpResponseRedirect(reverse("representantes"))    

# Ver un representante
def representante_entry(request, representante_id):
    return render(request, "academy/representantes.html", {
        "representante": Representante.objects.get(id=representante_id),
    })  

# Actualizar un representante
def representante_edit(request, representante_id):
    if (request.method == 'POST'):
        representante = Representante.objects.get(id=representante_id)
        representante.nombre = request.POST['nombre']
        representante.apellido = request.POST['apellido']
        representante.save()
        return HttpResponseRedirect(reverse("representantes"))     


# Tutores

# Listar los tutores
def tutores(request):
    return render(request, "academy/tutores.html", {
        "tutores": Tutor.objects.all(),
    })    

# Crear un nuevo tutor
def tutor_new(request):
    if (request.method == 'POST'):
        tutor = Tutor()
        tutor.nombre = request.POST['nombre']
        tutor.apellido = request.POST['apellido']
        tutor.save()
        return HttpResponseRedirect(reverse("tutores"))    

# Eliminar un tutor
def tutor_delete(request, tutor_id):
    tutor = Tutor.objects.get(id=tutor_id)
    tutor.delete()
    return HttpResponseRedirect(reverse("tutores"))    

# Ver un tutor
def tutor_entry(request, tutor_id):
    return render(request, "academy/tutores.html", {
        "tutor": Tutor.objects.get(id=tutor_id),
    })    

# Actualizar un tutor
def tutor_edit(request, tutor_id):
    if (request.method == 'POST'):
        tutor = Tutor.objects.get(id=tutor_id)
        tutor.nombre = request.POST['nombre']
        tutor.apellido = request.POST['apellido']
        tutor.save()
        return HttpResponseRedirect(reverse("tutores"))

# APIs           

def api_asistencias(request, alumno_id):
    if request.method == 'GET':
        alumno = Alumno.objects.get(id=alumno_id)
        # Asistencia.objects.filter(alumno=alumno)
        asistencias = listar_alumnos_por_fecha_de_asistencia()
        print(asistencias)
        return JsonResponse({
            "asistencias": listar_asistencias(alumno_id)
        }, status=201)
    else:
        return JsonResponse({
            "asistencias": listar_alumnos_por_fecha_de_asistencia()
        }, status=201)


def api_inactivar_alumnos(request):
    if request.method == 'GET':
        alumnos = Alumno.objects.all()
        for alumno in alumnos:
            if True:
                alumno.status = alumno.ACTIVO
                alumno.save()
        return JsonResponse({
            "message": f"se inactivaron tanto alumnos"
        }, status=201)


# def cargar_pago(request, alumno_id=None):
#     if request.method == 'GET':
#         return render(request, "academy/cargar_pago.html", {
#             "variable": 'mantenimiento'
#         })
#     elif request.method == 'POST':
#         return HttpResponse("Metodo no manejado")
#     else:
#         return HttpResponse("Metodo no manejado")

def asistencia(request):
    if request.method == 'GET':
        return render(request, "academy/asistencia.html", {
            "alumnos": listar_alumnos_por_fecha_de_asistencia(),
        })
    elif request.method == 'POST':
        print(request.POST['fecha'])
        alumno = Alumno.objects.get(id=request.POST['alumno_id'])
        alumno.status = alumno.ACTIVO
        alumno.save()
        asistencia = Asistencia(alumno=alumno, fecha=request.POST['fecha'])
        asistencia.save()
        return HttpResponseRedirect(reverse("asistencia"))
    else:
        return HttpResponse("Metodo no manejado")

def mantenimiento(request):
    return render(request, "academy/index.html", {
        "mostrar": 'mantenimiento'
    })

# Alumnos



def crear_alumno(nombre, apellido):
    nuevo = Alumno(nombre=nombre, apellido=apellido)
    nuevo.save()


def actualizar_perfil(perfil):
    print(perfil['id'])
    objeto = Alumno.objects.get(id=perfil['id'])
    objeto.nombre = perfil['nombre']
    objeto.apellido = perfil['apellido']
    objeto.save()

def contar_asistencias_hoy(alumno):
    ultimo_pago = Pago.objects.filter(alumno=alumno).order_by('-fecha_pago').first()
    ultimo_pago.fecha_inicio




def api_representante(request, representante_id):
    if request.method == 'GET':
        representante = Representante.objects.get(id=representante_id)
        return JsonResponse({
            "representante": representante
        }, status=201)

# def crear_representante(request, alumno_id):
#     if request.method == 'GET':
#         return render(request, "academy/perfil.html", {
#             "alumno": Alumno.objects.get(id=alumno_id),
#         })
#     elif (request.method == 'POST'):
#         nuevo = Representante()
#         nuevo.nombre = request.POST['nombre']
#         nuevo.apellido = request.POST['apellido']
#         nuevo.celular = request.POST['celular']
#         nuevo.email = request.POST['email']
#         nuevo.save()
#         alumno = Alumno.objects.get(id=alumno_id)
#         alumno.representante = nuevo
#         alumno.save()
#         return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def api_asociar_representante(request, alumno_id, representante_id):
    if request.method == 'POST':
        alumno = Alumno.objects.get(id=alumno_id)
        representante = Representante.objects.get(id=representante_id)
        alumno.representante = representante
        alumno.save()
        return JsonResponse({
            "message": f"se asocio el representante {representante.nombre} al alumno {alumno.nombre}"
        }, status=201)

    # if request.method == 'POST':
    #     alumno = Alumno.objects.get(id=alumno_id)
    #     representante = Representante.objects.get(id=representante_id)
    #     alumno.representante = representante
    #     alumno.save()
    #     return HttpResponseRedirect(reverse("index"))

def pagar(request, alumno_id=None):
    if request.method == 'GET':
        return render(request, "academy/cargar_pago.html", {
            "alumno": Alumno.objects.get(id=alumno_id),
        })
    elif (request.method == 'POST'):
        nuevo_pago = Pago()
        nuevo_pago.alumno = Alumno.objects.get(id=alumno_id)
        nuevo_pago.fecha_pago = request.POST["fecha_pago"]
        nuevo_pago.total_clases = request.POST["total_clases"]
        nuevo_pago.fecha_inicio = request.POST["fecha_inicio"]
        nuevo_pago.monto = request.POST["monto"]
        nuevo_pago.save()
        return HttpResponseRedirect(reverse("index"))


# def index(request):
#     if request.method == 'POST':
#         crear_alumno(request.POST["nombre"], request.POST["apellido"])
#         return HttpResponseRedirect(reverse("index"))
#     else:
#         return render(request, "academy/index.html", {
#             "alumnos": listar_alumnos_por_fecha_de_asistencia(),
#             "mostrar": 'index'
#         })


# Autenticación

# login
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

# logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# register
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
