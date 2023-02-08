# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # index GET lista los alumnos, POST crea un alumno
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),    
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),  
    path("asistencia", views.asistencia, name="asistencia"),
    # editar-alumno
    path("editar-alumno/<int:id>", views.editar_alumno, name="editar_alumno"),
    path("pagar/<int:alumno_id>", views.pagar, name="pagar"),
    path("mantenimiento", views.mantenimiento, name="mantenimiento"),
    # cargar-pago
    path("cargar-pago", views.cargar_pago, name="cargar_pago"),

    # Api Routes
    path("api/asistencias/<int:alumno_id>", views.api_asistencias, name="api_asistencias"), 
    path("api/inactivar_alumnos", views.api_inactivar_alumnos, name="api_inactivar_alumnos"),
]

