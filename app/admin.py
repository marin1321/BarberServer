from django.contrib import admin

# Register your models here.
from .models import *

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre_cat",)

class ServiciosAdmin(admin.ModelAdmin):
    model = Servicio
    list_display = ("tipoServicio", "valor", "idCategoria")

class ClientesAdmin(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "telefono", "email", "foto", "rol", "state")

class TrabajadoresAdmin(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "nom_local", "direccion", "telefono", "foto", "idCategoria", "email", "rol")

class CitasAdmin(admin.ModelAdmin):
    list_display = ("idCliente", "idServicio", "horaRegistroCita", "fechaRegistroCita")

class HorarioAdmin(admin.ModelAdmin):
    list_display = ("idTrabajador", "horaInicio", "fecha", "horaFinalizacion", "estado")

class calificacionAdmin(admin.ModelAdmin):
    list_display = ("idTrabajador", "idCliente", "numeroCalificacion", "comentario")

admin.site.register(Servicio, ServiciosAdmin)
admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Trabajadores, TrabajadoresAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(citas, CitasAdmin)
admin.site.register(horarios, HorarioAdmin)
admin.site.register(calificacion, calificacionAdmin)