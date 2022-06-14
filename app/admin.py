from django.contrib import admin

# Register your models here.
from .models import *

class ServiciosAdmin(admin.ModelAdmin):
    model = Servicio
    list_display = ("tipoServicio", "valor")

class ClientesAdmin(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "telefono", "email", "foto", "rol", "state")

class TrabajadoresAdmin(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "nom_local", "direccion", "telefono", "foto", "idCategoria", "email", "rol")

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre_cat", "idServicio",)

class CitasAdmin(admin.ModelAdmin):
    list_display = ("idTrabajador", "idCliente", "idCliente", "hora", "fecha")

admin.site.register(Servicio, ServiciosAdmin)
admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Trabajadores, TrabajadoresAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(citas, CitasAdmin)
