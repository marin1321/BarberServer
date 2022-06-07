from dataclasses import field, fields
from django import forms
from .models import *

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Trabajadores
        fields = ["nombres", "apellidos", "telefono", "email", "foto", "password", "nom_local", "direccion", "idCategoria"]