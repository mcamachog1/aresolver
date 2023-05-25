from datetime import datetime
from .models import User, Alumno, Asistencia, Pago, Representante, Tutor, Academia

# recibe: la academia que está consultando a sus alumnos y string de busqueda opcional
# retorna: una lista de registros
# registro = {
#   alumno: objeto alumno,
#   id: id del alumno, (redundante solo sirve para llamadas api)
#   nombre: nombre del alumno (redundante solo sirve para llamadas api)
#   fecha: fecha de ultima asistencia
#   status: status del alumno 
# }
# Lista los alumnos por orden de asistencia de mas reciente a mas antiguo
def listar_alumnos_por_fecha_de_asistencia(academia, qstr=""):
    alumnos_fecha_mas_reciente = []
    if qstr:
        alumnos = (Alumno.objects.filter(academias = academia,apellido__icontains = qstr) 
        | Alumno.objects.filter(academias = academia, nombre__icontains = qstr))
    else:
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

# Tipo de dato que retorna: Fecha
# Retorna la fecha de inicio de sesiones cubiertas con el ultimo pago
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
# Retorna el total de sesiones vistas después del ultimo pago
def ultimas_asistencias(alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    fecha_inicio_ultimo_ciclo = ultimo_inicio_de_clases(alumno_id)
    # sampledate__gte=datetime.date(2011, 1, 1)
    asistencias = Asistencia.objects.filter(fecha__gte=fecha_inicio_ultimo_ciclo, alumno=alumno)
    total = 0
    for asistencia in asistencias:
        total += asistencia.cantidad_sesiones
    return total

# Tipo de dato que retorna: Objeto Tutor de la ultima asistencia
# Recibe: id del alumno
def tutor_ultima_asistencia(alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    ultima_asistencia = Asistencia.objects.filter(alumno=alumno).order_by("-fecha").first()
    if ultima_asistencia:
        return ultima_asistencia.tutor
    else:
        return Tutor.objects.all().first()

# Recibe el request
# Devuelve la academia del usuario logueado
# Ojo ¿Qué pasa si se loguea un alumno con 2 o mas academias?
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

def total_pagos_por_mes(academia,year,month):
    return Pago.objects.filter(academia=academia, fecha_pago__year=str(year), fecha_pago__month=str(month)).count()

def total_clases_vistas_por_mes(academia,year,month):
    return Asistencia.objects.filter(academia=academia, fecha__year=str(year), fecha__month=str(month)).count()

def total_clases_pagadas_por_mes(academia,year,month):
    pagos = Pago.objects.filter(academia=academia, fecha_pago__year=str(year), fecha_pago__month=str(month))
    total = 0
    for pago in pagos:
        total += pago.total_clases
    return total

def total_montos_por_mes(academia,year,month):
    pagos = Pago.objects.filter(academia=academia, fecha_pago__year=str(year), fecha_pago__month=str(month))
    total = 0
    for pago in pagos:
        total += pago.monto
    return total



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

# recibe: lista de objetos pago
# retorna: una lista de diccionarios para convertir a JSON
# registro = {
#   alumno: nombre del alumno
#   fecha_pago: fecha de pago
#   monto: monto del pago
#   clases_pagadas: total clases pagadas
#   fecha_inicio: fecha de inicio de las clases pagadas
# }
# uso: para que la funcion api_pagos(month, year) retorne el formato exacto que necesita el template pagos.html
def tabla_pagos(pagos):
    registros = []
    for pago in pagos:
        registro = {
            "id": pago.id,
            "nombre": f"{Alumno.objects.get(id=pago.alumno.id).nombre} {Alumno.objects.get(id=pago.alumno.id).apellido}",
            "fecha_pago": pago.fecha_pago.strftime('%Y-%m-%d'),
            "monto": str(pago.monto),
            # "total_clases": pago.total_clases,
            "total_clases": '{0:.2g}'.format(pago.total_clases),
            "fecha_inicio": pago.fecha_inicio.strftime("%a %d-%m-%Y")
        }
        registros.append(registro)
    return registros