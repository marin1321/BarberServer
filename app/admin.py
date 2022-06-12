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
    list_display = ("nombres", "apellidos", "telefono", "email", "foto","rol")

class TrabajadoresAdmin(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "nom_local", "direccion", "telefono", "foto", "idCategoria", "email", "rol")

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre_cat", "idServicio",)

class CitasAdmin(admin.ModelAdmin):
    list_display = ("idTrabajador", "idCliente", "idCliente", "hora", "fecha")

admin.site.register(Servicios, ServiciosAdmin)
admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Trabajadores, TrabajadoresAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(citas, CitasAdmin)