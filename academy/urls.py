# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # index es alumnos.html
    path("", views.index, name="index"),
    path("alumnos", views.alumnos, name="alumnos"),

    # autenticación
    path("login", views.login_view, name="login"),    
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),  
    
    # asistencias
    path("asistencias", views.asistencias, name="asistencias"),
    path("asistencia_manual_alumno/<int:alumno_id>", views.asistencia_manual_alumno, name="asistencia_manual_alumno"),
    path("asistencia_new", views.asistencia_new, name="asistencia_new"),
    path("asistencia_entry/<int:asistencia_id>", views.asistencia_entry, name="asistencia_entry"),    
    path("asistencia_delete/<int:asistencia_id>", views.asistencia_delete, name="asistencia_delete"),
    path("asistencia_alumno/<int:alumno_id>", views.asistencia_alumno, name="asistencia_alumno"),
    
    # alumnos
    path("alumnos", views.alumnos, name="alumnos"),
    # path("alumnos/<str:qstr>", views.alumnos, name="alumnos"),
    path("alumno_new", views.alumno_new, name="alumno_new"),
    path("alumno_entry/<int:alumno_id>", views.alumno_entry, name="alumno_entry"),
    path("alumno_edit/<int:alumno_id>", views.alumno_edit, name="alumno_edit"),    
    path("alumno_delete/<int:alumno_id>", views.alumno_delete, name="alumno_delete"),
    
    # representantes
    path("representantes", views.representantes, name="representantes"),
    path("representante_new", views.representante_new, name="representante_new"),
    path("representante_entry/<int:representante_id>", views.representante_entry, name="representante_entry"),
    path("representante_edit/<int:representante_id>", views.representante_edit, name="representante_edit"),    
    path("representante_delete/<int:representante_id>", views.representante_delete, name="representante_delete"),

    # cursos
    path("cursos", views.cursos, name="cursos"),
    path("curso_entry/<int:curso_id>", views.curso_entry, name="curso_entry"),
    path("curso_new", views.curso_new, name="curso_new"),
    path("curso_edit/<int:curso_id>", views.curso_edit, name="curso_edit"),
    path("curso_delete/<int:curso_id>", views.curso_delete, name="curso_delete"),

    # tutores
    path("tutores", views.tutores, name="tutores"),
    path("tutor_entry/<int:tutor_id>", views.tutor_entry, name="tutor_entry"),
    path("tutor_new", views.tutor_new, name="tutor_new"),
    path("tutor_edit/<int:tutor_id>", views.tutor_edit, name="tutor_edit"),
    path("tutor_delete/<int:tutor_id>", views.tutor_delete, name="tutor_delete"),

    # pagos
    path("pagos", views.pagos, name="pagos"),    
    path("pago_new", views.pago_new, name="pago_new"),  
    path("pago_delete/<int:pago_id>", views.pago_delete, name="pago_delete"),  
    path("pagos_alumno/<int:alumno_id>", views.pagos_alumno, name="pagos_alumno"),  
    # path("asociar-representante/<int:alumno_id>/<int:representante_id>/", views.asociar_representante, name="asociar_representante"),
    path("pagar/<int:alumno_id>", views.pagar, name="pagar"),
    path("mantenimiento", views.mantenimiento, name="mantenimiento"),
    path("enviar_email", views.enviar_email, name="enviar_email"),
    # cargar-pago
    # path("cargar-pago", views.cargar_pago, name="cargar_pago"),
    
    # emails

    # Api Routes
    path("api/asistencias/<int:alumno_id>", views.api_asistencias, name="api_asistencias"), 
    path("api/asociar_representante/<int:alumno_id>/<int:representante_id>", views.api_asociar_representante, name="api_asociar_representante"), 
    path("api/inactivar_alumnos", views.api_inactivar_alumnos, name="api_inactivar_alumnos"),
    path("api/alumno_entry/<int:alumno_id>", views.api_alumno_entry, name="api_alumno_entry"), 
    path("api/pagos/<int:month>/<int:year>", views.api_pagos, name="api_pagos"),
    path("api/pagos/<int:month>/<int:year>/<int:alumno_id>", views.api_pagos, name="api_pagos"),


]

