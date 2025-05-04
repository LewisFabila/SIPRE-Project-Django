from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def login(request): #First View
    if request.method == "POST":
        usuario = request.POST["usuario"]
        password = request.POST["password"]
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("menu-admin")
        else:
            return render(request, "index.html", {"error": "EL NOMBRE DE USUARIO O CONTRASEÑA ES INCORRECTO"})
    return render(request, "index.html")

@login_required
def menu_admin(request):
    return render(request, "menu-admin.html", {"user": request.user})

def cerrar_sesion(request):
    logout(request)
    return redirect('/login')