from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import *
from .models import *

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

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