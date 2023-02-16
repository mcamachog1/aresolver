from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User, Alumno, Asistencia, Pago, Representante


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



def editar_alumno(request, id):
    sin_representante = False
    if request.method == 'GET':
        ultimo_pago = Pago.objects.filter(alumno=Alumno.objects.get(id=id)).order_by('-fecha_pago').first()
        # ultimo_pago.fecha_inicio
        mi_representante = Alumno.objects.get(id=id).representante
        if mi_representante is None :
            sin_representante = True
        return render(request, "academy/perfil.html", {
            "alumno": Alumno.objects.get(id=id),
            "representantes": Representante.objects.all(),
            "pagos": Pago.objects.filter(alumno=Alumno.objects.get(id=id)).order_by('-fecha_pago'),
            "sin_representante": sin_representante,
            "clases_vistas": "clases_vistas"
        })
    elif (request.method == 'POST'):
        perfil = {"id": id,
                  "nombre": request.POST["nombre"],
                  "apellido": request.POST["apellido"]}
        # print (perfil)
        actualizar_perfil(perfil)
        return HttpResponseRedirect(reverse("index"))

def api_representante(request, representante_id):
    if request.method == 'GET':
        representante = Representante.objects.get(id=representante_id)
        return JsonResponse({
            "representante": representante
        }, status=201)

def crear_representante(request, alumno_id):
    if request.method == 'GET':
        return render(request, "academy/perfil.html", {
            "alumno": Alumno.objects.get(id=alumno_id),
        })
    elif (request.method == 'POST'):
        nuevo = Representante()
        nuevo.nombre = request.POST['nombre']
        nuevo.apellido = request.POST['apellido']
        nuevo.celular = request.POST['celular']
        nuevo.email = request.POST['email']
        nuevo.save()
        alumno = Alumno.objects.get(id=alumno_id)
        alumno.representante = nuevo
        alumno.save()
        return HttpResponseRedirect(reverse("index"))

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


# Listar los alumnos por orden de asistencia mas reciente
def listar_alumnos_por_fecha_de_asistencia():
    # Crear estructura
    alumnos_fecha_mas_reciente = []
    # Seleccionar los alummnos
    alumnos = Alumno.objects.all()
    # Recorrer los alumnos y crear registro con alumno y fecha mas reciente de asistencia
    for alumno in alumnos:
        asistencia = Asistencia.objects.filter(
            alumno=alumno).order_by("-fecha").first()
        if asistencia is not None:
            fecha_str = asistencia.fecha.strftime("%a %d-%m-%Y")
        else:
            fecha_str = alumno.fecha_creacion.strftime("%a %d-%m-%Y")
        registro = {"alumno": alumno, "id": alumno.id, "nombre": f"{alumno.nombre} {alumno.apellido}",
                    "fecha": fecha_str, "status": alumno.get_status_display()}
        alumnos_fecha_mas_reciente.append(registro)
    return (alumnos_fecha_mas_reciente)

# Listar los alumnos por orden de asistencia mas reciente


def listar_asistencias(alumno_id):
    # Seleccionar los alummnos
    asistencias = []
    alumno = Alumno.objects.get(id=alumno_id)
    query_set = Asistencia.objects.filter(alumno=alumno).order_by("-fecha")
    for asistencia in query_set:
        if asistencia is not None:
            fecha_str = asistencia.fecha.strftime("%a %d-%m-%Y")
        else:
            fecha_str = alumno.fecha_creacion.strftime("%a %d-%m-%Y")
        registro = {"id": alumno.id, "nombre": f"{alumno.nombre} {alumno.apellido}",
                    "fecha": fecha_str, "status": alumno.get_status_display()}
        asistencias.append(registro)
    return (asistencias)


def index(request):
    if request.method == 'POST':
        crear_alumno(request.POST["nombre"], request.POST["apellido"])
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "academy/index.html", {
            "alumnos": listar_alumnos_por_fecha_de_asistencia(),
            "mostrar": 'index'
        })


def actualizar_representante(request, id):
    if request.method == 'POST':
        representante = Representante.objects.get(id=id)
        if 'salvar' in request.POST:
            representante.nombre = request.POST["nombre"]
            representante.apellido = request.POST["apellido"]
            representante.save()
            
        elif 'eliminar' in request.POST:
            representante.delete()
        return HttpResponseRedirect(reverse("representante"))
    elif request.method == 'GET':
        return render(request, "academy/representante.html", {
            "representantes": Representante.objects.all(),
            "representante": Representante.objects.get(id=id),
        })

def representante(request):
    if request.method == 'POST':
        nuevo = Representante()
        nuevo.nombre = request.POST["nombre"]
        nuevo.apellido = request.POST["apellido"]
        nuevo.save()
        return HttpResponseRedirect(reverse("representante"))
    else:
        return render(request, "academy/representante.html", {
            "representantes": Representante.objects.all(),
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
