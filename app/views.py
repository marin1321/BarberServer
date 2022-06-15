from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import *
from .models import *

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def sobreNosotros(request):
    return render(request, 'sobreNosotros.html')

def barber(request):
    barber = Trabajadores.objects.all()
    data = {
        "barber":barber
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
    global user_id 
    user_id = request.user.id
    usuarioActivo = User.objects.get(id=user_id)
    datosB = Trabajadores.objects.filter(email=usuarioActivo)
    data = {
        'datosB':datosB,
    }
    return render(request, 'perfilBarbero.html', data)

def perfilCliente(request):
    global user_id 
    user_id = request.user.id
    usuarioActivo = User.objects.get(id=user_id)
    datosC = Clientes.objects.filter(email=usuarioActivo)
    data = {
        'datosC':datosC,
    }
    return render(request, 'perfilCliente.html', data)

def registro(request):
    data = {
        "form":RegistrationForm
    }
    if request.method=='POST':
        formulario = RegistrationForm(data=request.POST, files=request.FILES)
        email = request.POST.get('email')
        if User.objects.filter(username=email).exists():
            return redirect(to="login")
        else:
            if formulario.is_valid():
                nombres = request.POST.get('nombres')
                apellidos = request.POST.get('apellidos')
                telefono = request.POST.get('telefono')
                email = request.POST.get('email')
                foto=request.FILES.get('foto')
                password = request.POST.get('password')
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
                    barbero.save()
                    user = User.objects.create_user(email, email, password)
                    login(request, user)
                    request.session['id'] = user.id
                    return redirect(to="perfilB")
                else:
                    cliente = Clientes()
                    cliente.nombres=nombres
                    cliente.apellidos=apellidos
                    cliente.telefono=telefono
                    cliente.email=email
                    cliente.foto=foto
                    cliente.password=password
                    cliente.rol="Cliente"
                    cliente.save()
                    user = User.objects.create_user(email, email, password)
                    login(request, user)
                    request.session['id'] = user.id
                    return redirect(to="perfilC")
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
        id_usuario = Trabajadores.objects.get(id=user_id)
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

def eliminarCuenta(request):
    global user_id 
    user_id = request.user.id
    usuarioActivo = User.objects.get(id=user_id)
    if Trabajadores.objects.filter(email=usuarioActivo).exists()==True:
        id = Trabajadores.objects.get(email=usuarioActivo).id
        usuario = get_object_or_404(Trabajadores, id=id)
        usuario.delete()
    if Clientes.objects.filter(email=usuarioActivo).exists()==True:
        id = Clientes.objects.get(email=usuarioActivo).id
        usuario = get_object_or_404(Clientes, id=id)
        usuario.delete()
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
    return render(request, 'contacto.html')
