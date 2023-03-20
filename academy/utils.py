from datetime import datetime
from .models import User, Alumno, Asistencia, Pago, Representante, Tutor, Academia

# recibe: la academia que está consultando a sus alumnos
# retorna: una lista de registros
# registro = {
#   alumno: objeto alumno,
#   id: id del alumno, (redundante solo sirve para llamadas api)
#   nombre: nombre del alumno (redundante solo sirve para llamadas api)
#   fecha: fecha de ultima asistencia
#   status: status del alumno 
# }
# Lista los alumnos por orden de asistencia de mas reciente a mas antiguo
def listar_alumnos_por_fecha_de_asistencia(academia):
    alumnos_fecha_mas_reciente = []
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

# Tipo de dato que retorna: Numero
# Retorna el total de clases pagadas en el ultimo pago (pago por adelantado)
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

# Tipo de dato que retorna: Numero
# Retorna el total de clases vistas después del ultimo pago
def ultimas_asistencias(alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    fecha_inicio_ultimo_ciclo = ultimo_inicio_de_clases(alumno_id)
    print(fecha_inicio_ultimo_ciclo)
    # sampledate__gte=datetime.date(2011, 1, 1)
    asistencias = Asistencia.objects.filter(fecha__gte=fecha_inicio_ultimo_ciclo, alumno=alumno)
    return asistencias.count()

# Tipo de dato que retorna: Objeto Tutor de la ultima asistencia
# Recibe: id del alumno
def tutor_ultima_asistencia(alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    ultima_asistencia = Asistencia.objects.filter(alumno=alumno).order_by("-fecha").first()
    return ultima_asistencia.tutor    


def obtener_academia(request):
    if request:
        if request.user.id is None:
            return False
        else:
            # Obtener el usuario logueado
            usuario = User.objects.get(id=request.user.id)
            # Validar el tipo de usuario logueado
            if usuario.tipo_de_usuario == usuario.DIRECTOR :
                return Academia.objects.get(director=request.user.id)
            # Si no es director ve los datos de Dummy
            elif usuario.tipo_de_usuario != usuario.DIRECTOR :
                return Academia.objects.get(nombre="Dummy")                
            else :
                return False
    else:
        return False

# Funciones usadas en las views

def total_pagado_por_mes(academia,anio,mes):
    return 52

def total_clases_por_mes(academia,anio,mes):
    return 4




# Funciones del API

# recibe: alumno y academia de donde quiero obtener las asistencias
# retorna: lista de registros para retornar JSON
#   registro = {nombre: nombre completo del alumno, fecha: fecha de la asistencia,
#               tutor: nombre del tutor, academia: nombre de la academia} 
def datos_tabla_asistencia(alumno, academia):
    asistencias = Asistencia.objects.filter(alumno=alumno,academia=academia).order_by("-fecha")
    data = []
    for a in asistencias:
        registro = {
            "id": a.id,
            "nombre": f"{a.alumno.nombre} {a.alumno.apellido}",
            "fecha": a.fecha,
            "tutor": f"{a.tutor.nombre} {a.tutor.apellido}",
            "academia": f"{a.academia.nombre}",
        }
        data.append(registro)
    return(data)        