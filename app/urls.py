from django.urls import path
from .views import *

urlpatterns=[
    path('', inicio, name='inicio'),
    path('perfil/', perfil, name='perfil'),
    path('perfil_barbero/', perfilBarbero, name='perfilB'),
    path('perfil_cliente/', perfilCliente, name='perfilC'),
    path('registrar/', registro, name='registro'),
]
