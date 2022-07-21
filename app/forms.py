from dataclasses import field, fields
from pyexpat import model
from django import forms
from django.forms import ValidationError
from .models import *

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Trabajadores
        fields = ["nombres", "apellidos", "telefono", "email", "foto", "password", "nom_local", "direccion", "idCategoria"]

class EditarClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ["nombres", "apellidos", "telefono", "foto"]
class EditarBarberoForm(forms.ModelForm):
    class Meta:
        model = Trabajadores
        fields = ["nombres", "apellidos", "telefono", "foto", "nom_local", "direccion", "idCategoria"]
        
class HorariosBarbero(forms.ModelForm):
    class Meta:
        model = horarios
        fields = ["horaInicio", "fecha", "horaFinalizacion"]

class Citas(forms.ModelForm):
    class Meta:
        model = citas
        fields = ["idServicio","horaRegistroCita", "fechaRegistroCita", "idHorario"]
        
class EditarHorarios(forms.ModelForm):
    class Meta:
        model = horarios
        fields = ["horaInicio","fecha"]