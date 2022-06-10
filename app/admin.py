from django.contrib import admin

# Register your models here.
from .models import *

class ServiciosAdmin(admin.ModelAdmin):
    model = Servicios
    list_display = ("tipoServicio", "valor")

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

class ClientesAdmin(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "telefono", "email", "rol")

admin.site.register(Servicios, ServiciosAdmin)
admin.site.register(Clientes)
admin.site.register(Trabajadores)
admin.site.register(Categoria)
admin.site.register(citas)