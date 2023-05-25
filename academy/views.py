from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core import serializers
from django.core.mail import send_mail
# from django import forms


from pprint import pprint
from datetime import date

import inspect
import json
# import requests
from decimal import Decimal
# import decimal
import csv

from datetime import datetime
from .models import User, Alumno, Asistencia, Pago, Representante, Tutor, Academia, Curso
from .utils import *
from mysite.secret_settings import MAILGUN_KEY

from .forms import NuevaAsistenciaForm

# Variables Globales

ACADEMIA = -1

# Asistencias

# Listar asistencias
def asistencias(request):
    if request.method == 'GET':
        academia = obtener_academia(request)
        return render(request, "academy/asistencias.html", {
            "alumnos": Alumno.objects.filter(academias=academia).order_by("nombre"),
            "tutores": Tutor.objects.filter(academia=academia).order_by("nombre"),
            "academias": Academia.objects.all(),
            "asistencias": Asistencia.objects.filter(academia=academia).order_by("-fecha"),
            "academia": academia,
            "form": NuevaAsistenciaForm
            
        })

# Crear una nueva asistencia
def asistencia_new(request):
    if (request.method == 'POST'):
        alumno = Alumno.objects.get(id=request.POST['alumno_id'])
        alumno.status = alumno.ACTIVO
        alumno.save()
        asistencia = Asistencia()
        asistencia.alumno=alumno
        asistencia.fecha=request.POST['fecha']
        asistencia.tutor=Tutor.objects.get(id=request.POST['tutor_id'])
        asistencia.curso=Curso.objects.get(id=request.POST['curso_id'])
        asistencia.cantidad_sesiones=request.POST['cantidad_sesiones']
        asistencia.academia= obtener_academia(request)
        # Academia.objects.get(id=request.POST['academia_id'])
        asistencia.save()
        return HttpResponseRedirect(reverse("alumno_entry", kwargs={"alumno_id":alumno.id}))

# Crear una nueva asistencia express conociendo al alumno
# manteniendo sus ultimos valores (academia, tutor y curso)
def asistencia_alumno(request, alumno_id):
    if (request.method == 'POST'):
        alumno = Alumno.objects.get(id=alumno_id)
        alumno.status = alumno.ACTIVO
        alumno.save()
        asistencia = Asistencia()
        asistencia.alumno=alumno
        now = datetime.now()
        asistencia.fecha= now.date()
        asistencia.tutor=Asistencia.objects.filter(alumno=alumno).order_by("-fecha").first().tutor
        asistencia.academia=Asistencia.objects.filter(alumno=alumno).order_by("-fecha").first().academia
        asistencia.curso=Asistencia.objects.filter(alumno=alumno).order_by("-fecha").first().curso
        asistencia.cantidad_sesiones = 1
        asistencia.save()
        return HttpResponseRedirect(reverse("alumno_entry", kwargs={"alumno_id":alumno_id}))

# Crear una nueva asistencia manual conociendo al alumno
# despliega el template de asistencias, seleccionando en la lista desplegable el alumno
# que hizo el requerimiento
def asistencia_manual_alumno(request, alumno_id):
    if (request.method == 'GET'):
        alumno = Alumno.objects.get(id=alumno_id)
        academia = obtener_academia(request)
        return render(request, "academy/asistencias.html", {
            "alumno": alumno,
            "tutor": tutor_ultima_asistencia(alumno_id),
            "academias": Academia.objects.all(),
            "asistencias": Asistencia.objects.filter(academia=academia, alumno=alumno).order_by("-fecha"),
            "academia": academia,
            "tutores": Tutor.objects.all(),
            "form": NuevaAsistenciaForm(initial={'alumno_id': alumno.id})
        })        
        
# Ver una asistencia
def asistencia_entry(request, asistencia_id):
    alumno = Asistencia.objects.get(id=asistencia_id).alumno
    return render(request, "academy/asistencias.html", {
        "asistencia": Asistencia.objects.get(id=asistencia_id),
        "asistencias": Asistencia.objects.filter(alumno=alumno).order_by("-fecha"),
     })  


# Eliminar asistencia
def asistencia_delete(request, asistencia_id):
    asistencia = Asistencia.objects.get(id=asistencia_id)
    alumno_id = asistencia.alumno.id
    asistencia.delete()
    url = request.headers['Referer']
    if "alumno" in url:
        return HttpResponseRedirect(reverse("alumno_entry", kwargs={"alumno_id":alumno_id}))
    elif "asistencias" in url:
        return HttpResponseRedirect(reverse("asistencias"))
    # pprint(inspect.getmembers(request))

# Pagos

# Listar los pagos
def pagos(request):
    # Ojo que pasa si la fecha no devuelve registros? La tabla no se pinta y da error
    month = date.today().month 
    year = date.today().year
    academia = obtener_academia(request)
    total_pagos = total_montos_por_mes(academia,year,month)
    total_clases = total_clases_pagadas_por_mes(academia,year,month)
    
    return render(request, "academy/pagos.html", {
        "pagos": Pago.objects.filter(academia=academia, fecha_pago__year=str(year), fecha_pago__month=str(month)).order_by("-fecha_pago"),
        "alumnos": Alumno.objects.filter(academias=academia),
        "total_pagos": total_pagos,
        "total_clases": total_clases,
        "cursos": Curso.objects.all(),
        "academia": academia  
    })

# Listar los pagos de un alumno 
def pagos_alumno(request, alumno_id):
    month = date.today().month 
    year = date.today().year
    return render(request, f"academy/pagos.html", {
        "pagos": Pago.objects.filter(alumno=Alumno.objects.get(id=alumno_id), fecha_pago__year=str(year), fecha_pago__month=str(month)).order_by("-fecha_pago"),
        "alumno": Alumno.objects.get(id=alumno_id),
        # "alumnos": Alumno.objects.all(),
        "cursos": Curso.objects.all(),
        "academia": obtener_academia(request)
    })    

# Crear nuevo pago  
def pago_new(request):
    academia = obtener_academia(request)
    if (request.method == 'POST'):
        alumno = Alumno.objects.get(id=request.POST["alumno_id"])
        curso = Curso.objects.get(id=request.POST["curso_id"])
        costo = float(curso.costo_por_sesion)
        pago = Pago()
        pago.alumno = alumno
        pago.fecha_pago = request.POST["fecha_pago"]
        pago.fecha_inicio = request.POST["fecha_inicio"]
        pago.monto = float(request.POST["monto"])
        print(type(pago.monto))
        print(type(costo))
        pago.curso = curso
        print(type(pago.monto/costo))
        pago.total_clases = pago.monto/costo
        pago.save()
        pago.academia = academia
        pago.save()
        return HttpResponseRedirect(reverse("pagos")) 

# Eliminar un pago
def pago_delete(request, pago_id):
    pago = Pago.objects.get(id=pago_id)
    pago.delete()
    return HttpResponseRedirect(reverse("pagos"))   

# Alumnos

# Listar los alumnos. Si qstr es vacio, los lista todos
# Esta pagina es la equivalente a index
def alumnos(request):

    academia = obtener_academia(request)
    if academia:
        if request.method == 'POST':
            return render(request, "academy/alumnos.html", {
                "alumnos": listar_alumnos_por_fecha_de_asistencia(academia, request.POST["qstr"]),
                "academia": academia        
            })          
        else:
            return render(request, "academy/alumnos.html", {
                "alumnos": listar_alumnos_por_fecha_de_asistencia(academia),   
                "academia": academia       
            })  
    else:
        print("SALIENDO POR AQUI")
        return render(request, "academy/login.html")
      



# Crear un nuevo alumno
def alumno_new(request):
    if (request.method == 'POST'):
        academia = Academia.objects.get(director=request.user.id)        
        alumno = Alumno()
        alumno.nombre = request.POST['nombre']
        alumno.apellido = request.POST['apellido']
        alumno.save()
        alumno.academias.add(academia)
        alumno.save()
        return HttpResponseRedirect(reverse("alumnos"))    

# Eliminar un alumno 
def alumno_delete(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    alumno.delete()
    return HttpResponseRedirect(reverse("alumnos"))   

# Ver un alumno
def alumno_entry(request, alumno_id):
    if ultimas_clases_pagadas(alumno_id) != 0:
        porcentaje = round(ultimas_asistencias(alumno_id) / ultimas_clases_pagadas(alumno_id) * 100,2)
    else:
        if ultimas_asistencias(alumno_id) > 0:
            porcentaje = 100
        else:
            porcentaje = 0
    asistencias = Asistencia.objects.filter(alumno=Alumno.objects.get(id=alumno_id)).order_by("-fecha")
    paginator = Paginator(asistencias, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pagos = Pago.objects.filter(alumno=Alumno.objects.get(id=alumno_id))
    total_monto_pagado = 0
    total_monto_clases_vistas = 0
    for pago in pagos:
        total_monto_pagado += pago.monto
    asistencias = Asistencia.objects.filter(alumno=Alumno.objects.get(id=alumno_id))
    for asistencia in asistencias:
        total_monto_clases_vistas += asistencia.cantidad_sesiones * 1  if asistencia.curso is None  else asistencia.curso.costo_por_sesion
    return render(request, "academy/alumnos.html", {
        "alumno": Alumno.objects.get(id=alumno_id),
        "representantes": Representante.objects.all().order_by("nombre"),
        "asistencias": page_obj,
        "pagos": Pago.objects.filter(alumno=Alumno.objects.get(id=alumno_id)).order_by("-fecha_pago"),
        "ultimas_clases_pagadas": ultimas_clases_pagadas(alumno_id),
        "ultimas_asistencias": ultimas_asistencias(alumno_id),
        "porcentaje": porcentaje,
        "academia": obtener_academia(request),
        "total_monto_pagado": total_monto_pagado,
        "total_monto_clases_vistas": total_monto_clases_vistas,
        "saldo": total_monto_pagado - total_monto_clases_vistas,

    })  

# Actualizar un alumno
def alumno_edit(request, alumno_id):
    if (request.method == 'POST'):
        perfil = {
            "id": alumno_id,
            "nombre": request.POST["nombre"],
            "apellido": request.POST["apellido"],
            "email": request.POST["email"]
            }
        actualizar_perfil(perfil)
        if 'representante_id' in request.POST:
            alumno = Alumno.objects.get(id=alumno_id)
            alumno.representante = Representante.objects.get(id=request.POST['representante_id'])
            alumno.save()
        return HttpResponseRedirect(reverse("alumno_entry", kwargs={"alumno_id":alumno_id}))

# Representantes

# Listar los representantes
def representantes(request):
    academia = obtener_academia(request)
    print(academia)
    return render(request, "academy/representantes.html", {
        "representantes": Representante.objects.filter(academia=academia).order_by("nombre"),
        "sexo_opciones": Representante.SEXO_CHOICES,
        "academia": academia,
    })  

# Crear un nuevo representante
def representante_new(request):
    academia = obtener_academia(request)
    if (request.method == 'POST'):
        representante = Representante()
        representante.nombre = request.POST['nombre']
        representante.apellido = request.POST['apellido']
        representante.email = request.POST['email']
        representante.academia = academia
        representante.sexo = request.POST['sexo']
        representante.save()
        
        # Al crear el representante se asocia al alumno si se recibe el id
        if 'alumno_id' in request.POST:
            alumno = Alumno.objects.get(id=request.POST['alumno_id'])
            alumno.representante = representante
            alumno.save()
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
        "sexo_opciones": Representante.SEXO_CHOICES,
        "academia": obtener_academia(request),        
    })  

# Actualizar un representante
def representante_edit(request, representante_id):
    if (request.method == 'POST'):
        representante = Representante.objects.get(id=representante_id)
        representante.nombre = request.POST['nombre']
        representante.apellido = request.POST['apellido']
        representante.email = request.POST['email']
        representante.sexo = request.POST['sexo']        
        representante.save()
        return HttpResponseRedirect(reverse("representantes"))     

# Tutores

# Listar los tutores
def tutores(request):
    academia = obtener_academia(request)
    return render(request, "academy/tutores.html", {
        "tutores": Tutor.objects.filter(academia=academia).order_by("nombre"),
        "academia": academia,
    })    

# Crear un nuevo tutor
def tutor_new(request):
    academia = obtener_academia(request)
    if (request.method == 'POST'):
        tutor = Tutor()
        tutor.nombre = request.POST['nombre']
        tutor.apellido = request.POST['apellido']
        tutor.academia = academia
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
        "academia": obtener_academia(request),
    })    

# Actualizar un tutor
def tutor_edit(request, tutor_id):
    if (request.method == 'POST'):
        tutor = Tutor.objects.get(id=tutor_id)
        tutor.nombre = request.POST['nombre']
        tutor.apellido = request.POST['apellido']
        tutor.save()
        return HttpResponseRedirect(reverse("tutores"))


def actualizar_perfil(perfil):
    print(perfil['id'])
    objeto = Alumno.objects.get(id=perfil['id'])
    objeto.nombre = perfil['nombre']
    objeto.apellido = perfil['apellido']
    objeto.email = perfil['email']
    objeto.save()

# def contar_asistencias_hoy(alumno):
#     ultimo_pago = Pago.objects.filter(alumno=alumno).order_by('-fecha_pago').first()
#     ultimo_pago.fecha_inicio

def mantenimiento(request):
    return render(request, "#", {
        "mostrar": 'mantenimiento'
    })




def pagar(request):
    send_mail(
        'Subject here',
        'Here is the message.',
        'mcamachog@gmail.com',
        ['aresolveronline@gmail.com'],
        fail_silently=False,
    )


# Enviar emails

def enviar_email(request):
    # Cree el objeto HttpResponse con el encabezado CSV apropiado.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="correos.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['correo','nombre','mensaje_1','mensaje_2','mensaje_3'])

    for r in Representante.objects.filter(academia=obtener_academia(request)):
        saludo = "Bienvenid@ " #actualmente el campo es NULL, valor por defecto
        saludo = "Bienvenida " if r.sexo == r.FEMENINO else "Bienvenido "
        mensaje_1 = saludo + 'a la comunidad de AResolver. Por este canal recibiras contenidos relacionados con matematica y programacion.'
        mensaje_2='He guardado tu email porque has sido cliente de mis clases de matematica o de programacion.'
        mensaje_3=''
        writer.writerow([f'{r.email}', f'{r.nombre}', mensaje_1, mensaje_2, mensaje_3])

    return response

    # response = requests.post(
    #     "https://api.mailgun.net/v3/sandbox2af4dcd6e41d4024a1522aa0a418be39.mailgun.org/messages",
    #     auth=("api", MAILGUN_KEY),
    #     data={"from": "Maryví <postmaster@aresolveronline.com>",
    #           "to": ["mcamachog@hotmail.com"],
    #           "subject": "Hello",
    #           "text": "Ocultando Clave MAILGUN"})
    # json = response.json()
    print(MAILGUN_KEY)
    return HttpResponse('ok')






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
            ACADEMIA = obtener_academia(request)
            return HttpResponseRedirect(reverse("alumnos"))
        else:
            return render(request, "academy/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "academy/login.html")

# logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("alumnos"))

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
        return HttpResponseRedirect(reverse("alumnos"))
    else:
        return render(request, "academy/register.html")

# APIs           

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

def api_asistencias(request, alumno_id):
    if request.method == 'GET':
        academia = obtener_academia(request)
        alumno = Alumno.objects.get(id=alumno_id)
        asistencias = datos_tabla_asistencia(alumno, academia)
        return JsonResponse({"asistencias": asistencias}, safe=False, status=200)
    
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

def api_pagos(request, month, year, alumno_id=None):
    academia = obtener_academia(request)
    total_pagos_mes = total_pagos_por_mes(academia,year,month)
    total_clases_mes = total_clases_pagadas_por_mes(academia,year,month)
    total_monto_mes = total_montos_por_mes(academia,year,month)
    if not alumno_id: 
        pagos_pintar = tabla_pagos(Pago.objects.filter(academia=academia, fecha_pago__year=str(year), fecha_pago__month=str(month)).order_by("-fecha_pago"))
        pagos = json.dumps(pagos_pintar)
    else:
        pagos_pintar = tabla_pagos(Pago.objects.filter(academia=academia, alumno=Alumno.objects.get(id=alumno_id), fecha_pago__year=str(year), fecha_pago__month=str(month)).order_by("-fecha_pago"))
        pagos = json.dumps(pagos_pintar)
    print(alumno_id)
    return JsonResponse({
        "pagos": pagos,
        "alumno": alumno_id,
        "total_pagos_mes": total_pagos_mes,
        "total_clases_mes": total_clases_mes,
        "total_monto_mes": total_monto_mes,
        "message": f"se llamo api pagos con mes {month} y año {year}"
        }, status=201)  
  
def api_representante(request, representante_id):
    if request.method == 'GET':
        representante = Representante.objects.get(id=representante_id)
        return JsonResponse({
            "representante": representante
        }, status=201)

def api_alumno_entry(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    nombre = f"{alumno.nombre} {alumno.apellido}"
    if request.method == 'GET':
        return JsonResponse({
            "nombre": nombre
        }, status=201)
