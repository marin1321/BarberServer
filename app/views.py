from ast import If
from cgi import print_form
import email
import imp
from multiprocessing import AuthenticationError
import re
from tokenize import String
from django.contrib import messages
from django.conf import settings
from django.forms import DateInput
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import *
from .models import *
from datetime import datetime, date
import time
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
fechaHoy = datetime.today().strftime('%Y-%m-%d')
def loginF(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "logueado con exito!")
            print("logueado con exito!")
            return redirect('/perfilCliente.html')

        else:
            print("Credenciales incorrectas")
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
        data = 0
        usuarioActivo = User.objects.get(id=user_id)
        if Trabajadores.objects.filter(email=usuarioActivo).exists()==True:
            datas = Trabajadores.objects.filter(email=usuarioActivo)
            data = {
                "dataT": datas 
            }
        else:
            if Clientes.objects.filter(email=usuarioActivo).exists()==True:
                datas = Clientes.objects.filter(email=usuarioActivo)
                data = {
                    "dataC": datas 
                }
        print(data)
        if data != 0:        
            return render(request, 'inicio.html', data)
        else:
            return render(request, 'inicio.html')
    else:
        return render(request, 'inicio.html')

def sobreNosotros(request):
    if request.user.is_authenticated:
        global user_id
        user_id = request.user.id
        usuarioActivo = User.objects.get(id=user_id)
        data = 0
        if Trabajadores.objects.filter(email=usuarioActivo).exists()==True:
            datas = Trabajadores.objects.filter(email=usuarioActivo)
            data = {
                "dataT": datas 
            }
        else:
            if Clientes.objects.filter(email=usuarioActivo).exists()==True:
                datas = Clientes.objects.filter(email=usuarioActivo)
                data = {
                    "dataC": datas 
                }
        if data != 0:
            return render(request, 'sobreNosotros.html', data)
        else:
            return render(request, 'sobreNosotros.html')
    else:
        return render(request, 'sobreNosotros.html')

def barber(request):
    barber = Trabajadores.objects.filter(state = "activo")
    categorias = Categoria.objects.all()
    searchs = request.GET.get('search')
    select = request.GET.get('opciones')
    calificaciones = calificacion.objects.all()
    listIdT = []
    promedioC = []
    for idBarberos in barber:
        listIdT.append(idBarberos.id)
        numeroCalificaciones = []
        if len(calificaciones) >= 1:
            for idCalificacion in calificaciones:
                if idBarberos == idCalificacion.idTrabajador:
                    numeroCalificaciones.append(idCalificacion.numeroCalificacion)
            if len(numeroCalificaciones) >0:          
                sumcalificacion = sum(numeroCalificaciones)
                promedios = sumcalificacion // len(numeroCalificaciones)
                promedioC.append(promedios)
            else:
                promedioC.append(0)
    dictCalificacion = dict(zip(listIdT, promedioC))
    if request.user.is_authenticated:
        global user_id
        user_id = request.user.id
        usuarioActivo = User.objects.get(id=user_id)
        datas = 0
        if Trabajadores.objects.filter(email=usuarioActivo).exists()==True:
            datas = Trabajadores.objects.get(email=usuarioActivo).rol
        elif Clientes.objects.filter(email=usuarioActivo).exists()==True:
            idUsr = Clientes.objects.get(email=usuarioActivo)
            datas = idUsr.rol
    nombreSelect=None
    pasarC = 0
    if searchs:
        if select != None and select != 'Todos':
            select = Categoria.objects.get(nombre_cat = select).id
            barber= Trabajadores.objects.filter(Q(nombres__icontains = searchs)|Q(apellidos__icontains = searchs),idCategoria = select).distinct()
            nombreSelect=select
            pasarC = 1
        else:
            barber= Trabajadores.objects.filter(Q(nombres__icontains = searchs)|Q(apellidos__icontains = searchs)).distinct()
    if select and nombreSelect == None and pasarC == 1:
        select = Categoria.objects.get(nombre_cat = select).id
        barber = Trabajadores.objects.filter(idCategoria = select)
        nombreSelect = select
    if request.method == "POST":
        idsTrabajador = request.POST.get('idTrabajadores')
        result  = request.POST.get('result')
        comentarios= request.POST.get('sugerencia')
        if int(result) > 5:
            print("Error Hoho")
        else: 
            calificacionDatos = calificacion()
            calificacionDatos.idCliente = idUsr
            calificacionDatos.idTrabajador = Trabajadores.objects.get(id = idsTrabajador)
            calificacionDatos.numeroCalificacion = int(result)
            calificacionDatos.comentario = comentarios
            calificacionDatos.save()
    if datas != 0:
        data = {
            "barber":barber,
            "categoria":categorias,
            "rol":datas,
            "select": nombreSelect,
            "dicCalificacion":dictCalificacion,
        } 
    else:
        data = {
            "barber":barber,
            "categoria":categorias,
            "select": nombreSelect,
            "dicCalificacion":dictCalificacion,
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
        idTrabajador = Trabajadores.objects.get(email=usuarioActivo)
        selectT =  request.GET.get('TiempoSelect')
        selectE = request.GET.get('estados')
        datosCita = getBarberosClientes(selectE, selectT, "trabajador", idTrabajador)
        data = {
            'datosB':datosB,
            "datosCita":datosCita,
            "selectH": selectT,
            "selectE": selectE,
        }
        print("AQUI --> " +str(request.user))
        if request.method == "POST":
            peticion = request.POST.get('peticion')
            trabajador =  Trabajadores.objects.get(email=usuarioActivo)
            estado =  request.POST.get("estado")
            if estado == "activo":
                trabajador.state = "activo"
                trabajador.save()
            elif estado == "inactivo":
                trabajador.state = "inactivo"
                trabajador.save()
            else:
                idCita = request.POST.get('idCita')
                idCita =  citas.objects.get(id=idCita)
                idCita.peticion = peticion
                idCita.save()
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
        selectT =  request.GET.get('TiempoSelect')
        selectE = request.GET.get('estados')
        citasId = getBarberosClientes(selectE, selectT, "cliente", idCliente)
        if request.method == "POST":
            user =  Clientes.objects.get(email=usuarioActivo)
            estado =  request.POST.get("estado")
            peticion = request.POST.get('peticion')
            citaPeticion = request.POST.get('idCita')
            if citaPeticion != None:
                citaPeticion = citas.objects.get(id = citaPeticion)
                citaPeticion.peticion = peticion
                citaPeticion.save()
            else:
                if estado == "activo":
                    user.state = "activo"
                    user.save()
                elif estado == "inactivo":
                    user.state = "inactivo"
                    user.save()
                else:
                    idCita = request.POST.get('idCita')
                    idCita =  citas.objects.get(id=idCita)
                    idCita.peticion = "inactivo"
                    idCita.save()
        data = {
            'citas':citasId,
            'datosC':datosC,
            'selectH':selectT,
            'selectE':selectE,
        }
        return render(request, 'perfilCliente.html', data)
    else:
        return redirect(to="login")

def getBarberosClientes(selectE, selectT,rol, ids):
    datosSelect = []
    print(rol == "trabajador")
    print('ID',selectE)
    if selectE != None:
        if rol == "trabajador":
            if selectE == "aceptada":
                datosCita = citas.objects.filter(idTrabajador = ids, peticion = 'aceptada')
            elif selectE == "pendiente":
                print(4)
                datosCita = citas.objects.filter(idTrabajador = ids, peticion = 'pendiente')
            elif selectE == "cancelada":
                datosCita = citas.objects.filter(idTrabajador = ids, peticion = 'cancelada')
        elif rol == "cliente":
            if selectE == "aceptada":
                datosCita = citas.objects.filter(idCliente = ids, peticion = 'aceptada')
            elif selectE == "pendiente":
                datosCita = citas.objects.filter(idCliente = ids, peticion = 'pendiente')
            elif selectE == "cancelada":
                datosCita = citas.objects.filter(idCliente = ids, peticion = 'cancelada')
        else:
            if selectE == "todos":
                if rol == "trabajador":
                    datosCita = citas.objects.filter(idTrabajador = ids)
                elif rol == "cliente":
                    datosCita = citas.objects.filter(idCliente = ids)
    print("Dias estado",selectT != None and selectT != 'todos')
    print('Estado select',selectT )
    if selectT != None and selectT != 'todos':
        if selectT == 'estaSemana':
            semanaHoy =sacarSemana(int(fechaHoy[0:4]),int(fechaHoy[5:7]), int(fechaHoy[8:10]))
            for datoCita in datosCita:
                fechaDeCita = datoCita.idHorario.fecha 
                if int(fechaHoy[0:4]) == int(fechaDeCita.year):
                    semanaCita = sacarSemana(int(fechaDeCita.year),int(fechaDeCita.month), int(fechaDeCita.day))
                    if semanaHoy == semanaCita:
                        datosSelect.append(datoCita)
        elif selectT == 'hoy':
            for datoCita in datosCita:
                fechaDeCita = datoCita.idHorario.fecha 
                if fechaHoy == fechaDeCita:
                    datosSelect.append(datoCita)
        elif selectT == 'esteMes':
            for datoCita in datosCita:
                fechaDeCita = datoCita.idHorario.fecha 
                if int(fechaHoy[0:4]) == int(fechaDeCita.year) and int(fechaHoy[5:7]) == int(fechaDeCita.month):
                    datosSelect.append(datoCita)
        elif selectT == 'esteAnio':
            for datoCita in datosCita:
                fechaDeCita = datoCita.idHorario.fecha
                if int(fechaHoy[0:4]) == int(fechaDeCita.year):
                    datosSelect.append(datoCita)
    if len(datosSelect) == 0 and selectE == None and selectT == None:
        if rol == "traba-jador":
            datosSelect = citas.objects.filter(idTrabajador = ids)
        elif rol == "cliente":
            datosSelect = citas.objects.filter(idCliente = ids)
    elif len(datosSelect) == 0 and selectE == "todos" and selectT == "todos":
        if rol == "trabajador":
            datosSelect = citas.objects.filter(idTrabajador = ids)
        elif rol == "cliente":
            datosSelect = citas.objects.filter(idCliente = ids)
    elif len(datosSelect) == 0 and selectE != "todos"and selectT == "todos":
        datosSelect = datosCita
    return datosSelect

def sacarSemana (año, mes, dia):
    dt = date(año, mes, dia) 
    wk = dt.isocalendar()[1]
    return wk

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
        formulario = RegistrationForm(data=request.POST)
        email = request.POST.get('email')
        if User.objects.filter(username=email).exists():
            messages.success(request, "El correo electronico ya se encuentra logueado")
        else:
            if formulario.is_valid():
                nombres = request.POST.get('nombres')
                apellidos = request.POST.get('apellidos')
                telefono = request.POST.get('telefono')
                foto=request.POST.get('foto')
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
        inicioHora = request.POST.get('horaInicio')
        inicioHora = inicioHora.strip()
        horaHoy = time.strftime("%H:%M")
        desdeFecha =  request.POST.get('desdeFecha')
        hastaFecha = request.POST.get('hastaFecha')
        inputInfo = request.POST.get('inputInfo')
        hora2 = inicioHora[3:5]
        hora1 = inicioHora[0:2]
        print(inputInfo == '1')
        if inputInfo == '1':
            if inicioHora:
                hora2 = int(hora2) + 30
                fecha = request.POST.get('fecha')
                fecha =  fecha.strip()
                if int(fecha[0:4]) >= int(fechaHoy[0:4]):
                    restaAñosUnDia = int(fecha[0:4]) - int(fechaHoy[0:4])
                    if restaAñosUnDia <= 1:
                        restaMeses = int(fecha[5:7]) - int(fechaHoy[5:7])
                        if restaMeses >= 1:
                            if int(hora1) < 22:
                                tiempo(hora1,hora2,id_usuario,inicioHora,fecha)
                                print("Sexto if")                            
                        elif int(fechaHoy[5:7]) == int(fecha[5:7]):
                            if  int(fecha[8:10]) >= int(fechaHoy[8:10]):
                                if int(horaHoy[0:2]) > int(hora1):
                                    then =  datetime(int(fechaHoy[0:4]), int(fechaHoy[5:7]), int(fechaHoy[8:10]), int(horaHoy[0:2]), int(horaHoy[3:5], 0))
                                    now =  datetime(int(fecha[0:4]), int(fecha[5:7]), int(fecha[8:10]), int(inicioHora[0:2]), int(inicioHora[3:5], 0))
                                    tiempoMinutos = obtenerDiferencias(then,now, 'mins')
                                    if tiempoMinutos >= 90:
                                        if int(hora1) < 22:
                                            tiempo(hora1,hora2,id_usuario,inicioHora,fecha)
                                        else:
                                            print("La hora pasa de los limites de tiempo")
                                    else:
                                        print("La hora que colocaste no cumple con el reglamiento ")
                                else:
                                    print("No puede ser antes de la hora de hoy")
                            else:
                                print("No colocar los dias antes")
                        else:
                            print("Esta fecha no es permitida")
                    else:
                        print("Mala fecha primera")
                else:
                    print("Mala la fecha")
            else:
                print("Llene los espacios")
        elif inputInfo == '0':
            if int(desdeFecha[0:4]) >= int(fechaHoy[0:4]):
                restaAños = int(hastaFecha[0:4]) - int(fechaHoy[0:4])
                if restaAños == 1:
                    if int(desdeFecha[5:7]) < 12 and int(hastaFecha[5:7]) > 1:
                        print("no puede escocger esta fecha")
                    else:
                        diasFaltantes = 31 - int(desdeFecha[8:10])
                        diasRestantes = diasFaltantes + int(hastaFecha[8:10])
                        forTiempo(diasRestantes,diasFaltantes,desdeFecha,hastaFecha, hora1, hora2, id_usuario, inicioHora)
                elif int(hastaFecha[0:4]) == int(fechaHoy[0:4]):
                    restaMeses = int(hastaFecha[5:7]) - int(desdeFecha[5:7]) 
                    if restaMeses == 1:
                        diasDesde = obtener_dias_del_mes(int(desdeFecha[5:7]), int(desdeFecha[0:4]))
                        diasFaltantes = diasDesde - int(desdeFecha[8:10])
                        diasRestantes = diasFaltantes + int(hastaFecha[8:10])
                        forTiempo(diasRestantes,diasFaltantes,desdeFecha,hastaFecha, hora1, hora2, id_usuario, inicioHora)
                    elif int(hastaFecha[5:7]) == int(desdeFecha[5:7]):
                        if int(desdeFecha[8:10]) >= int(fechaHoy[8:10]):
                            restaDias =  int(hastaFecha[8:10]) - int(desdeFecha[8:10])
                            forTiempo(restaDias,0,desdeFecha,hastaFecha, hora1, hora2, id_usuario, inicioHora)
                        else:
                            print("No es permitida")
                    else:
                        print("Esta fecha no es permitida")
            else:
                print("revise su fecha")
    return render(request, "horarioBarber.html", data)
    
def obtenerDiferencias(then, now = datetime.now()):

    duration = now - then
    duration_in_s = duration.total_seconds() 
    

    minute_ct = 60 

    def mins():
        return divmod(duration_in_s, minute_ct)[0]

    return  int(mins())


def forTiempo (diasRestantes, diasFaltantes, desdeFecha, hastaFecha, hora1, hora2, id_usuario, inicioHora):
    listaDias = [int(desdeFecha[8:10]), int(hastaFecha[8:10])]
    tiempo(hora1,hora2,id_usuario,inicioHora,desdeFecha)
    print("dias-->", diasRestantes)
    for dias in range(diasRestantes):
        print(5)
        # tiempo(hora1,hora2,id_usuario,inicioHora,desdeFecha )
        if diasFaltantes != 0:
            print(8)
            if diasFaltantes >= dias:
                listaDias[1] = listaDias[1] - 1 
                fecha = hastaFecha[0:4] + "-" + hastaFecha[5:7] + "-"+ str(listaDias[1])
                tiempo(hora1,hora2,id_usuario,inicioHora,fecha)
            else:
                listaDias[0] = listaDias[0] + 1 
                fecha = desdeFecha[0:4] + "-" + desdeFecha[5:7] + "-"+ str(listaDias[0])
                tiempo(hora1,hora2,id_usuario,inicioHora,fecha)
        else:
            print(3)
            listaDias[0] = listaDias[0] + 1 
            fecha = desdeFecha[0:4] + "-" + desdeFecha[5:7] + "-"+ str(listaDias[0])
            tiempo(hora1,hora2,id_usuario,inicioHora,fecha)
def tiempo (hora1,hora2,id_usuario,inicioHora,fecha):
    print(1)
    if int(hora2) >= 60:
            hora2 = int(hora2) - 60 
            hora1 = int(hora1) + 2
    else: 
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
def es_bisiesto(anio: int) -> bool:
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)
def obtener_dias_del_mes(mes: int, anio: int) -> int:
    # Abril, junio, septiembre y noviembre tienen 30
    if mes in [4, 6, 9, 11]:
        return 30
    # Febrero depende de si es o no bisiesto
    if mes == 2:
        if es_bisiesto(anio):
            return 29
        else:
            return 28
    else:
        # En caso contrario, tiene 31 días
        return 31
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
    idServicio = Servicio.objects.filter(idCategoria = barbero.idCategoria)
    data = {
        "horario":horario,
        "servicio":idServicio
    } 
    if request.method == 'POST':
        datosServicio = request.POST.get("datosServicio")
        print(datosServicio)
        horaRegistroCita = time.strftime("%H:%M:%Sq")
        horaRegistroCita = horaRegistroCita.strip()
        idHorario = request.POST.get('idHorario')
        fechaRegistroCita = datetime.today().strftime('%Y-%m-%d')
        fechaRegistroCita = fechaRegistroCita.strip()
        idHorario = idHorario.strip()
        idHorario =  horarios.objects.get(id=idHorario)
        mandarNotificacion(idHorario, idCliente, barbero)
        if citas.objects.filter(idHorario = idHorario ).exists():
            redirect(to="barberos")
        else:
            cita = citas()
            cita.idCliente = idCliente
            cita.idServicio = Servicio.objects.get(id = datosServicio)
            cita.horaRegistroCita = horaRegistroCita
            cita.fechaRegistroCita = fechaRegistroCita
            cita.idHorario = idHorario
            cita.idTrabajador = barbero
            cita.peticion = "pendiente"
            cita.save()
            idHorario.estado = "inactivo"
            idHorario.save()
            messages.success(request,"Tu cita se agendado")
    return render(request, "agendarPlugin.html", data)

def mandarNotificacion(idHorario, nombreCliente, barbero):
    inicioHorario = idHorario.horaInicio
    subject = 'Señor Barber usted tiene una cita a las: ' + str(inicioHorario)
    message = 'Quien Reservo la cita el cliente ' + nombreCliente.nombres 
    email_from =  settings.EMAIL_HOST_USER
    recipient_list = [barbero.email]
    print('si lo mando')
    send_mail(subject, message, email_from, recipient_list) 


def eliminarCuenta(request):
    global user_id 
    user_id = request.user.id
    usuarioActivo = User.objects.get(id=user_id)
    if Trabajadores.objects.filter(email=usuarioActivo).exists():
        id = Trabajadores.objects.get(email=usuarioActivo).id
        usuario = get_object_or_404(Trabajadores, id=id)

    if Clientes.objects.filter(email=usuarioActivo).exists():
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
    if Trabajadores.objects.filter(email=usuarioActivo).exists():
        datas = Trabajadores.objects.get(email=usuarioActivo).rol
    elif Clientes.objects.filter(email=usuarioActivo).exists():
        datas = Clientes.objects.get(email=usuarioActivo).rol
    id = Clientes.objects.get(email=usuarioActivo).id
    perfil = get_object_or_404(Clientes, id=id)
    data = {
        'rol':datas,
        'form': EditarClienteForm(instance=perfil),
    }
    if request.method=='POST':
        formulario = EditarClienteForm(data=request.POST, instance=perfil)
        if formulario.is_valid():
            foto=request.POST.get('foto')
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
    if Trabajadores.objects.filter(email=usuarioActivo).exists():
        datas = Trabajadores.objects.get(email=usuarioActivo).rol
    elif Clientes.objects.filter(email=usuarioActivo).exists():
        datas = Clientes.objects.get(email=usuarioActivo).rol
    id = Trabajadores.objects.get(email=usuarioActivo).id
    perfil = get_object_or_404(Trabajadores, id=id)
    data = {
        'rol':datas,
        'form': EditarBarberoForm(instance=perfil),
    }
    if request.method=='POST':
        estado =  request.POST.get("estado")
        formulario = EditarBarberoForm(data=request.POST, instance=perfil)
        if formulario.is_valid():
            foto=request.POST.get('foto')
            idTrabajador = Trabajadores.objects.get(email=usuarioActivo)
            idTrabajador.foto = foto
            formulario.save()
            return redirect(to="perfilB")
        elif estado == "activo":
            trabajador = Trabajadores()
            trabajador.estado = "activo"
            trabajador.save()
        elif estado == "inactivo":
            trabajador = Trabajadores()
            trabajador.estado = "inactivo"
            trabajador.save()
        else:
            data["form"] = formulario
    return render(request, 'editarPerfilB.html', data)

def modal_barber(request, id):
    barbero = Trabajadores.objects.filter( id = id )
    calificaciones = calificacion.objects.filter( idTrabajador = id)
    for dataCategoria in barbero:
        servicios = Servicio.objects.filter(idCategoria = dataCategoria.idCategoria)
    
    numeroCalificacion = 0
    promedioC = []
    if request.user.is_authenticated:
        global user_id
        user_id = request.user.id
        usuarioActivo = User.objects.get(id=user_id) 
        datas = 0
        if Trabajadores.objects.filter(email=usuarioActivo).exists()==True:
            idUsr = Trabajadores.objects.get(email=usuarioActivo)
            datas = idUsr.rol
        elif Clientes.objects.filter(email=usuarioActivo).exists()==True:
            idUsr = Clientes.objects.get(email=usuarioActivo)
            datas = idUsr.rol
    if len(calificaciones) >= 1:
        for idCalificacion in calificaciones:
            promedioC.append(idCalificacion.numeroCalificacion)
        sumcalificacion = sum(promedioC)
        numeroCalificacion = sumcalificacion // len(promedioC)
    print(numeroCalificacion)

    if datas != 0:
        data = {
            "dataT":barbero,
            "calificacion": numeroCalificacion,
            "rol":datas,
            "estrellitas":[1,2,3,4,5],
            "Dservicios":servicios,
        }
    else:
        data = {
            "dataT":barbero,
            "calificacion": numeroCalificacion,
            "estrellitas":[1,2,3,4,5],
            "Dservicios":servicios,
        }
    return render(request, 'modalB.html', data)
def modal_EdiH(request, id):
    print("-->",id)
    horariosIds = horarios.objects.get(id = id)
    idHorario = get_object_or_404(horarios, id=id)
    data = {
        "id": horariosIds,
        "form": EditarHorarios(instance=idHorario),
    } 
    print(request)
    return render(request, 'modalH.html', data)
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
    if request.user.is_authenticated:
        global user_id
        user_id = request.user.id
        usuarioActivo = User.objects.get(id=user_id)
        data = 0
        if Trabajadores.objects.filter(email=usuarioActivo).exists()==True:
            datas = Trabajadores.objects.filter(email=usuarioActivo)
            data = {
                "dataT": datas 
            }
        else:
            if Clientes.objects.filter(email=usuarioActivo).exists()==True:
                datas = Clientes.objects.filter(email=usuarioActivo)
                data = {
                    "dataC": datas 
                }
        if data != 0:
            return render(request, 'contacto.html', data)
        else:
            return render(request, 'contacto.html')
    else:
        return render(request, 'contacto.html') 

def verHorarios(request):
    global user_id 
    user_id = request.user.id
    usuarioActivo = User.objects.get(id=user_id)
    id_usuario = Trabajadores.objects.get(email=usuarioActivo)
    datosH = horarios.objects.filter(idTrabajador=id_usuario)
    datosB = Trabajadores.objects.filter(email=usuarioActivo)
    data = {
        'datosH':datosH,
        'datosB':datosB,
    }
    if request.method == 'POST':
        horarioId = request.POST.get('horarioId')
        idHorario = get_object_or_404(horarios, id=horarioId)
        formulario = EditarHorarios(data=request.POST, instance=idHorario)
        if formulario.is_valid():
            formulario.save()
        else:
            horarioId = request.POST.get('horarioId')
            horarioId = horarios.objects.get(id = horarioId)
            horarioId.estado = 'inactivo'
            horarioId.save()
    return render(request, 'verHorariosPlugin.html', data)
def eliminarHorario(request):
    if request.method=='POST':
        usuario = get_object_or_404(horarios, id=id)
        usuario.delete()
        return redirect(to="inicio")
    