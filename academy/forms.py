from django import forms
from .models import Alumno, Tutor, Curso

#Formularios
class DateInput(forms.DateInput):
    input_type = 'date'

class NuevaAsistenciaForm(forms.Form):
    # Lista desplegable Alumnos
    alumnos = Alumno.objects.filter(academias=1)
    opciones_alumno = []
    # opciones_alumno.append(("-1", "Seleccione un alumno:"))
    for alumno in alumnos:
        opcion = (alumno.id, alumno.nombre + " " + alumno.apellido)
        opciones_alumno.append(opcion)

    # Lista desplegable Tutores
    tutores = Tutor.objects.all()
    opciones_tutor = []
    # opciones_tutor.append(("-1", "Seleccione un tutor:"))
    for tutor in tutores:
        opcion = (tutor.id, tutor.nombre)
        opciones_tutor.append(opcion)
    
    # Lista desplegable Cursos
    cursos = Curso.objects.all()
    # print(cursos)
    opciones_curso = []
    for curso in cursos:
        opcion = (curso.id, curso.nombre)
        opciones_curso.append(opcion)

    # Campos de formulario
    alumno_id = forms.ChoiceField(choices = opciones_alumno, label="")
    curso_id = forms.ChoiceField(choices = opciones_curso, label="")
    tutor_id = forms.ChoiceField(choices = opciones_tutor, label="")
    fecha = forms.DateField(widget=DateInput, label="")
    cantidad_sesiones = forms.DecimalField(label="", widget=forms.NumberInput(attrs={'value': 1, 'title': 'Cantidad de Sesiones', 'width': '50px'}))
