from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

# Create your views here.

@login_required
def lista_usuarios(request):
    usuarios = User.objects.all().select_related()  # Optimiza consultas
    return render(request, "menu-usuarios.html", {"usuarios": usuarios})

@login_required
def eliminar_usuarios(request):
    if request.method == "POST":
        ids = request.POST.getlist('usuarios_seleccionados')
        User.objects.filter(id__in=ids).delete()
    return redirect('lista-usuarios')