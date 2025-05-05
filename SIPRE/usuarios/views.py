from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.hashers import make_password

# Create your views here.

@login_required
def lista_usuarios(request):
    usuarios = User.objects.all().select_related()  # Optimiza consultas
    grupos = Group.objects.all()
    return render(request, "menu-usuarios.html", {"usuarios": usuarios, "grupos": grupos,})

@login_required
def registrar_usuario(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        username = request.POST["usuario"]
        password = make_password(request.POST["password"])
        grupo_id = request.POST["grupo"]

        user = User.objects.create(
            username=username,
            first_name=nombre,
            password=password,
        )
        grupo = Group.objects.get(id=grupo_id)
        user.groups.add(grupo)
        return redirect("lista-usuarios")

@login_required
def eliminar_usuarios(request):
    if request.method == "POST":
        ids = request.POST.getlist('usuarios_seleccionados')
        User.objects.filter(id__in=ids).delete()
    return redirect('lista-usuarios')