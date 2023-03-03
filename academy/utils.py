from datetime import datetime
from .models import User, Alumno, Asistencia, Pago, Representante, Tutor, Academia

# Listar los alumnos por orden de asistencia mas reciente
def listar_alumnos_por_fecha_de_asistencia(academia):
    # Crear estructura
    alumnos_fecha_mas_reciente = []
    # Seleccionar los alummnos
    alumnos = Alumno.objects.filter(academias=academia)
    # Recorrer los alumnos y crear registro con alumno y fecha mas reciente de asistencia
    for alumno in alumnos:
        asistencia = Asistencia.objects.filter(
            alumno=alumno, academia=academia).order_by("-fecha").first()
        if asistencia is not None:
            fecha_str = asistencia.fecha.strftime("%a %d-%m-%Y")
        else:
            fecha_str = alumno.fecha_creacion.strftime("%a %d-%m-%Y")
        registro = {"alumno": alumno, "id": alumno.id, "nombre": f"{alumno.nombre} {alumno.apellido}",
                    "fecha": fecha_str, "status": alumno.get_status_display()}
        alumnos_fecha_mas_reciente.append(registro)
        alumnos_fecha_mas_reciente.sort(key=fecha_ultima_asistencia,reverse=True)
    return (alumnos_fecha_mas_reciente)

# Listar asistencias del alumno de mas reciente a mas antigua
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

# Funciones para presentar % de consumo de las clases
def ultimas_clases_pagadas(alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    ultimo_pago = Pago.objects.filter(alumno=alumno).order_by("fecha_pago").last()
    if ultimo_pago is None:
        return 0
    else:
       return ultimo_pago.total_clases

def ultimo_inicio_de_clases(alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    ultimo_pago = Pago.objects.filter(alumno=alumno).order_by("fecha_pago").last()
    if ultimo_pago is None:
        if Asistencia.objects.filter(alumno=alumno).order_by("fecha").first() is None:
            return Alumno.objects.get(id=alumno_id).fecha_creacion
        return Asistencia.objects.filter(alumno=alumno).order_by("fecha").first().fecha
    else: 
       return ultimo_pago.fecha_inicio

def fecha_ultima_asistencia(e):
    return datetime.strptime(e['fecha'], "%a %d-%m-%Y")


def ultimas_asistencias(alumno_id):

    alumno = Alumno.objects.get(id=alumno_id)
    fecha_inicio_ultimo_ciclo = ultimo_inicio_de_clases(alumno_id)
    print(fecha_inicio_ultimo_ciclo)
    # sampledate__gte=datetime.date(2011, 1, 1)
    asistencias = Asistencia.objects.filter(fecha__gte=fecha_inicio_ultimo_ciclo, alumno=alumno)
    return asistencias.count()


def obtener_academia(request):
    if request:
        if request.user.id is None:
            return False
        else:
            if User.objects.get(id=request.user.id).tipo_de_usuario == 'D' :
                return Academia.objects.get(director=request.user.id)
            else :
                return False
    else:
        return False