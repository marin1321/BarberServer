from django.db import models

# Create your models here.

class Servicios(models.Model):
    tipoServicio = models.CharField(max_length=50)
    valor = models.FloatField()

class Categoria(models.Model):
    nombre_cat = models.CharField(max_length=60)
    idServicio = models.ForeignKey(Servicios, on_delete=models.SET_NULL, blank=True, null=True)

class Trabajadores(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    nom_local = models.CharField(max_length=50)
    direccion = models.CharField(max_length=70)
    telefono = models.CharField(max_length=30)
    foto = models.ImageField(upload_to="trabajadores", blank=True, null=True)
    idCategoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True)
    rol = models.CharField(max_length=45)
    email = models.EmailField()
    password = models.CharField(max_length=200)

class Clientes(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    telefono = models.CharField(max_length=30)
    email = models.EmailField()
    foto = models.ImageField(upload_to="clientes", blank=True, null=True)
    password = models.CharField(max_length=100)
    rol = models.CharField(max_length=45)

class citas(models.Model):
    idTrabajador = models.ForeignKey(Trabajadores, on_delete=models.SET_NULL, blank=True, null=True)
    idCliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, blank=True, null=True)
    idServicio = models.ForeignKey(Servicios, on_delete=models.SET_NULL, blank=True, null=True)
    hora = models.TimeField()
    fecha = models.DateField()

    
