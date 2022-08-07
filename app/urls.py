from django.urls import path
from .views import *

urlpatterns=[
    path('', inicio, name='inicio'),
    path('sobre_nosotros/', sobreNosotros, name='sobreNosotros'),
    path('perfil/', perfil , name='perfil'),
    path('barberos/', barber, name='barberos'),
    path('modal_barberos/<id>/', modal_barber, name='modal_barberos'),
    path('modal_edith/<id>', modal_EdiH, name='modal_edith'),
    path('perfil_barbero/', perfilBarbero, name='perfilB'),
    path('perfil_cliente/', perfilCliente, name='perfilC'),
    path('citas_barbero/', citasBarbero, name='citasBarbero'),
    path('registrar/', registro, name='registro'),
    path('elimininar_cunta/', eliminarCuenta, name='inactivarCuenta'),
    path('editar_perfil_cliente/', editarPerfilC, name='editarPerfilC'),
    path('editar_perfil_barbero/', editarPerfilB, name='editarPerfilB'),
    path('contacto/', contacto, name='contactos'),
    path('horarios/', horarioBarber, name='horarios'),
    path('verHorario/', verHorarios, name='verHorario'),
    path('perdirCitas/<id>', cita, name='citas'),
    path('citasBarbero/', citasBarbero, name='citasbarber'),
    path('login/', loginF, name='login'),    
    path('chat/', chat),
    # path('eliminarHorario/', eliminarHorario, name='eliminarHorario'),
]
