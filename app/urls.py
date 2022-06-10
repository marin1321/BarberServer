from django.urls import path
from .views import *

urlpatterns=[
    path('', inicio, name='inicio'),
    path('sobre_nosotros/', sobreNosotros, name='sobreNosotros'),
    path('perfil/', perfil, name='perfil'),
    path('barberos/', barber, name='barberos'),
<<<<<<< HEAD
    path('modal_barberos/<id>/', modal_barber, name='modal_barberos'),
=======
    path('contactenos/', contactenos, name='contactenos'),
>>>>>>> 8e7ec368915b181ee4f04605a05fa6a9326cfb1c
    path('perfil_barbero/', perfilBarbero, name='perfilB'),
    path('perfil_cliente/', perfilCliente, name='perfilC'),
    path('registrar/', registro, name='registro'),
    path('elimininar_cunta/', eliminarCuenta, name='eliminarCuenta'),
    path('editar_perfil_cliente/', editarPerfilC, name='editarPerfilC'),
    path('editar_perfil_barbero/', editarPerfilB, name='editarPerfilB'),
    path('contacto/', contacto, name='contactos'),
]
