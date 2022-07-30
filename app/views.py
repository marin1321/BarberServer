import email
import imp
from multiprocessing import AuthenticationError
from django.contrib import messages
from arrow import now
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import *
from .models import *
from datetime import datetime
import time
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

def chat(request):
    return render(request, 'chat.html')

def loginF(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "logueado con exito!")
            return redirect('/perfilCliente.html')

        else:
            messages.warning(request, "Credenciales incorrectas")
    else:
        form = AuthenticationForm(request)
    context = {
        "form": form
    }
    return render(request, "registration/loginPrueba.html", context)

def inicio(request):
    if request.user.is_authenticated:
        global user_id
        user_id = request.user.id
        usuarioActivo = User.objects.get(id=user_id)
        if Trabajadores.objects.filter(email=usuarioActivo).exists()==True:
            datas = Trabajadores.objects.filter(email=usuarioActivo)
            data = {
                "datas": datas 
            }
        else:
            if Clientes.objects.filter(email=usuarioActivo).exists()==True:
                datas = Clientes.objects.filter(email=usuarioActivo)
                data = {
                    "datas": datas 
                }
        return render(request, 'inicio.html', data)
    else:
        return render(request, 'inicio.html')

def sobreNosotros(request):
    return render(request, 'sobreNosotros.html')

def barber(request):
    barber = Trabajadores.objects.all()
    categorias = Categoria.objects.all()
    searchs = request.GET.get('search')
    select = request.GET.get('opciones')
    if searchs:
        if select:
            print('hola')
        else:
            barber= Trabajadores.objects.filter(Q(nombres__icontains = searchs)|Q(apellidos__icontains = searchs)).distinct()
        
    data = {
        "barber":barber,
        "categoria":categorias,
    }  
     
    return render(request, 'barberos.html', data)

def perfil(request):
    global user_id
    user_id = request.user.id
    usuarioActivo = User.objects.get(id=user_id)
    if Trabajadores.objects.filter(email=usuarioActivo).exists()==True:
        return redirect(to="perfilB")
    if Clientes.objects.filter(email=usuarioActivo).exists()==True:
        return redirect(to="perfilC")

def perfilBarbero(request):
    if request.user.is_authenticated:
        global user_id 
        usuarioActivo = User.objects.get(id=user_id)
        datosB = Trabajadores.objects.filter(email=usuarioActivo)
        data = {
            'datosB':datosB,
        }

        return render(request, 'perfilBarbero.html', data)
    else:
        return redirect(to="login")

def perfilCliente(request):
    if request.user.is_authenticated:
        global user_id 
        user_id = request.user.id
        usuarioActivo = User.objects.get(id=user_id)
        datosC = Clientes.objects.filter(email=usuarioActivo)
        idCliente = Clientes.objects.get(email=usuarioActivo)
        citasId = citas.objects.filter(idCliente=idCliente)
        data = {
            'citas':citasId,
            'datosC':datosC,
        }
        return render(request, 'perfilCliente.html', data)
    else:
        return redirect(to="login")

def citasBarbero(request):
    global user_id 
    user_id = request.user.id
    usuarioActivo = User.objects.get(id=user_id)
    idTrabajador = Trabajadores.objects.get(email=usuarioActivo)
    datosCita = citas.objects.filter(idTrabajador = idTrabajador)
    data = {
        "datosCita":datosCita
    }
    if request.method=='POST':
        idCita = request.POST.get('idCita')
        idCita =  citas.objects.get(id=idCita)
        idCita.peticion = "cancelada"
        idCita.save()
    return render(request, 'citasBarbero.html', data)

def registro(request):
    data = {
        "form":RegistrationForm
    }
    if request.method=='POST':
        print("hola")
        formulario = RegistrationForm(data=request.POST, files=request.FILES)
        email = request.POST.get('email')
        if User.objects.filter(username=email).exists():
            messages.success(request, "El correo electronico ya se encuentra logueado")
        else:
            if formulario.is_valid():
                nombres = request.POST.get('nombres')
                apellidos = request.POST.get('apellidos')
                telefono = request.POST.get('telefono')
                foto=request.FILES.get('foto')
                password = request.POST.get('password')
                email = request.POST.get('email')
                idCategoria = request.POST.get('idCategoria')
                nom_local = request.POST.get('nom_local')
                direccion = request.POST.get('direccion')
                nombres = nombres.strip()
                apellidos = apellidos.strip()
                telefono = telefono.strip()
                email = email.strip()
                password = password.strip()
                idCategoria = idCategoria.strip()
                nom_local = nom_local.strip()
                direccion = direccion.strip()
                state = "activo"
                print("\n\n\n", idCategoria ,"\n\n\n")
                if idCategoria != "":
                    print("\n\n\n diferente \n\n\n")
                    barbero = Trabajadores()
                    barbero.nombres=nombres
                    barbero.apellidos=apellidos
                    barbero.telefono=telefono
                    barbero.email=email
                    barbero.foto=foto
                    barbero.password=password
                    barbero.rol="Barbero"
                    barbero.nom_local=nom_local
                    barbero.direccion=direccion
                    idCategoria = Categoria.objects.get(id=idCategoria)
                    barbero.idCategoria=idCategoria
                    barbero.state = state
                    barbero.save()
                    user = User.objects.create_user(email, email, password)
                    login(request, user)
                    request.session['id'] = user.id
                    return redirect(to="inicio")
                else:
                    cliente = Clientes()
                    cliente.nombres=nombres
                    cliente.apellidos=apellidos
                    cliente.telefono=telefono
                    cliente.email=email
                    cliente.foto=foto
                    cliente.password=password
                    cliente.rol="Cliente"
                    cliente.state = state
                    cliente.save()
                    user = User.objects.create_user(email, email, password)
                    login(request, user)
                    request.session['id'] = user.id
                    return redirect(to="inicio")
            else:
                data = {
                    "form":RegistrationForm
                }
    return render(request, 'registration/registrar.html', data)

def horarioBarber(request):
    data = {
        "form" : HorariosBarbero
    }
    if request.method=='POST':
        global user_id 
        user_id = request.user.id
        usuarioActivo = User.objects.get(id=user_id)
        id_usuario = Trabajadores.objects.get(email=usuarioActivo)
        print(id_usuario)
        inicioHora = request.POST.get('horaInicio')
        fecha = request.POST.get('fecha')
        fecha =  fecha.strip()
        inicioHora = inicioHora.strip()
        hora2 = inicioHora[3:5]
        hora2 = int(hora2) + 30
        if hora2 >= 60:
            hora2 = int(hora2) - 60
            hora1 = inicioHora[0:2]
            hora1 = int(hora1) + 2
        else: 
            hora1 = inicioHora[0:2]
            hora1 = int(hora1) + 1
        finalizarHora = str(hora1) + ":" + str(hora2)
        activo = "activo"
        horario = horarios()
        horario.idTrabajador = id_usuario
        horario.horaInicio = inicioHora
        horario.fecha = fecha
        horario.horaFinalizacion = finalizarHora
        horario.estado = activo
        horario.save()

    return render(request, "horarioBarber.html", data)

def cita(request, id):
    # data = {
    #     "form" : Citas 
    # }
    global user_id 
    user_id = request.user.id
    usuarioActivo = User.objects.get(id=user_id)
    idCliente =  Clientes.objects.get(email=usuarioActivo)
    horario = horarios.objects.filter( idTrabajador = id )
    barbero = Trabajadores.objects.get( id = id )
    data = {
        "horario":horario
    } 
    if request.method == 'POST':
        idCategoria = Trabajadores.objects.get( id = id ).idCategoria
        idCategoria = Categoria.objects.get(nombre_cat = idCategoria).idServicio
        idServicio = idCategoria
        horaRegistroCita = time.strftime("%H:%M:%Sq")
        horaRegistroCita = horaRegistroCita.strip()
        idHorario = request.POST.get('idHorario')
        fechaRegistroCita = datetime.today().strftime('%Y-%m-%d')
        print("Fecha registro -->", fechaRegistroCita)
        fechaRegistroCita = fechaRegistroCita.strip()
        idHorario = idHorario.strip()
        mandarNotificacion(idHorario, idCliente, barbero)
        idHorario =  horarios.objects.get(id=idHorario)
        cita = citas()
        cita.idCliente = idCliente
        cita.idServicio = idServicio
        cita.horaRegistroCita = horaRegistroCita
        cita.fechaRegistroCita = fechaRegistroCita
        cita.idHorario = idHorario
        cita.idTrabajador = barbero
        cita.peticion = "activo"
        cita.save()
        idHorario.estado = "inactivo"
        idHorario.save()
    return render(request, "agendar.html", data)

def mandarNotificacion(idHorario, nombreCliente, barbero):
    inicioHorario = horarios.objects.get(id = idHorario).horaInicio
    subject = 'Señor Barber usted tiene una cita a las: ' + str(inicioHorario)
    message = 'Quien Reservo la cita el cliente ' + nombreCliente.nombres 
    email_from =  settings.EMAIL_HOST_USER
    recipient_list = [barbero.email]
    send_mail(subject, message, email_from, recipient_list) 


def eliminarCuenta(request):
    global user_id 
    user_id = request.user.id
    usuarioActivo = User.objects.get(id=user_id)
    if Trabajadores.objects.filter(email=usuarioActivo).exists()==True:
        id = Trabajadores.objects.get(email=usuarioActivo).id
        usuario = get_object_or_404(Trabajadores, id=id)

    if Clientes.objects.filter(email=usuarioActivo).exists()==True:
        id = Clientes.objects.get(email=usuarioActivo).id
        state = Clientes.objects.get(state=usuarioActivo)
        usuario = get_object_or_404(Clientes, id=id)
        print("HOLA")
        
    usuarioActivo.delete()
    return redirect(to="inicio")

def editarPerfilC(request):
    global user_id 
    user_id = request.user.id
    usuarioActivo = User.objects.get(id=user_id)
    id = Clientes.objects.get(email=usuarioActivo).id
    perfil = get_object_or_404(Clientes, id=id)
    data = {
        'form': EditarClienteForm(instance=perfil),
    }
    if request.method=='POST':
        formulario = EditarClienteForm(data=request.POST, instance=perfil, files=request.FILES)
        if formulario.is_valid():
            foto=request.FILES.get('foto')
            idCliente = Clientes.objects.get(email=usuarioActivo)
            idCliente.foto = foto
            formulario.save()
            return redirect(to="perfilC")
        else:
            data["form"] = formulario
    return render(request, 'editarPerfilC.html', data)

def editarPerfilB(request):
    global user_id 
    user_id = request.user.id
    usuarioActivo = User.objects.get(id=user_id)
    id = Trabajadores.objects.get(email=usuarioActivo).id
    perfil = get_object_or_404(Trabajadores, id=id)
    data = {
        'form': EditarBarberoForm(instance=perfil),
    }
    if request.method=='POST':
        formulario = EditarBarberoForm(data=request.POST, instance=perfil, files=request.FILES)
        if formulario.is_valid():
            foto=request.FILES.get('foto')
            idTrabajador = Trabajadores.objects.get(email=usuarioActivo)
            idTrabajador.foto = foto
            formulario.save()
            return redirect(to="perfilB")
        else:
            data["form"] = formulario
    return render(request, 'editarPerfilB.html', data)

def modal_barber(request, id):
    barbero = Trabajadores.objects.filter( id = id )
    data = {
        "dataT":barbero
    } 
    return render(request, 'modalB.html', data)

def contacto(request):
    if request.method=='POST':
        firstName = request.POST.get('FirstName')
        Email = request.POST.get('Email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(message)
        phone = phone.strip()
        Email = Email.strip()
        subject = 'Comentario de parte: ' + firstName
        message = 'Numero de telefono ' + phone + ' correo electronico ' + str(Email) + ' Mensaje: ' + message
        email_from =  settings.EMAIL_HOST_USER
        recipient_list = ["barberserver123company@gmail.com"]
        send_mail(subject, message, email_from, recipient_list) 
    return render(request, 'contacto.html')

def verHorarios(request):
    global user_id 
    user_id = request.user.id
    usuarioActivo = User.objects.get(id=user_id)
    id_usuario = Trabajadores.objects.get(email=usuarioActivo)
    datosH = horarios.objects.filter(idTrabajador=id_usuario)
    datosB = Trabajadores.objects.filter(email=usuarioActivo)
    print('dattosB', datosB)
    data = {
        'datosH':datosH,
        'datosB':datosB,
    }
    return render(request, 'verHorarios.html', data)
def eliminarHorario(request):
    if request.method=='POST':
        usuario = get_object_or_404(horarios, id=id)
        usuario.delete()
        return redirect(to="inicio")
