# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),    
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),  
    path("asistencia", views.asistencia, name="asistencia"),  

    # Api Routes
    path("api/asistencias/<int:alumno_id>", views.api_asistencias, name="api_asistencias"), 
]

