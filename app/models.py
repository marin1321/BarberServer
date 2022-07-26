from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre_cat = models.CharField(max_length=60, blank=False, null=False)

    def __str__(self):
        return self.nombre_cat

class Servicio(models.Model):
    tipoServicio = models.CharField(max_length=50)
    idCategoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True)
    valor = models.FloatField()

class Trabajadores(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    nom_local = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=70, null=True, blank=True)
    telefono = models.CharField(max_length=30)
    foto = models.URLField(blank=True, null=True)
    idCategoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True)
    rol = models.CharField(max_length=45)
    email = models.EmailField()
    state = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=200)

class Clientes(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    telefono = models.CharField(max_length=30)
    email = models.EmailField()
    foto = models.URLField(blank=True, null=True)
    password = models.CharField(max_length=100)
    rol = models.CharField(max_length=45)
    state = models.CharField(max_length=30, null=True)

class horarios(models.Model):
    idTrabajador = models.ForeignKey(Trabajadores, on_delete=models.SET_NULL, blank=True, null=True)
    horaInicio = models.TimeField()
    fecha = models.DateField()
    horaFinalizacion = models.TimeField()
    estado =  models.CharField(max_length=30, null=True)

class citas(models.Model):
    idCliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, blank=True, null=True)
    idServicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, blank=True, null=True)
    horaRegistroCita = models.TimeField()
    fechaRegistroCita = models.DateField()
    idHorario = models.ForeignKey(horarios, on_delete=models.SET_NULL, blank=True, null=True)
    peticion =  models.CharField(max_length=30, null=True)
    idTrabajador = models.ForeignKey(Trabajadores, on_delete=models.SET_NULL, blank=True, null=True)

class calificacion(models.Model):
    idCliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, blank=True, null=True)
    idTrabajador = models.ForeignKey(Trabajadores, on_delete=models.SET_NULL, blank=True, null=True)
    numeroCalificacion = models.IntegerField(blank=True, null=True)