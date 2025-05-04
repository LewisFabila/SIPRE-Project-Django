from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.

def login(request): #Vista del Login
    if request.method == "POST":
        usuario = request.POST["usuario"]
        password = request.POST["password"]
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            auth_login(request, user)
            
            # Redireccion segun el tipo de usuario
            if user.groups.filter(name="Administrador").exists():
                return redirect("menu-admin")
            elif user.groups.filter(name="Finanzas").exists():
                return redirect("menu-finanzas")
            elif user.groups.filter(name="Contabilidad").exists():
                return redirect("menu-contabilidad")
            elif user.groups.filter(name="General").exists():
                return redirect("menu-general")
            else:
                return render(request, "index.html", {"error": "Usuario sin grupo asignado."})
            
        else:
            return render(request, "index.html", {"error": "EL NOMBRE DE USUARIO O CONTRASEÑA ES INCORRECTO"})
    return render(request, "index.html")

# Ubicacion del redireccionamiento
@login_required
def menu_admin(request):
    return render(request, "menu-admin.html", {"user": request.user})

@login_required
def menu_finanzas(request):
    return render(request, "menu-finanzas.html", {"user": request.user})

@login_required
def menu_contabilidad(request):
    return render(request, "menu-contabilidad.html", {"user": request.user})

@login_required
def menu_general(request):
    return render(request, "menu-general.html", {"user": request.user})

def cerrar_sesion(request): # Cierre de sesion
    logout(request)
    return redirect('/login')