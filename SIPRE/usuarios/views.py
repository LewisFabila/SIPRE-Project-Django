from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

@login_required
def lista_usuarios(request):
    usuarios = User.objects.all().select_related()  # Optimiza consultas
    grupos = Group.objects.all()

    # Peticiones de Busqueda usando GET
    busqueda = request.GET.get('busqueda', '')
    num_registros = request.GET.get('num_registros', 10)
    pagina = request.GET.get('page', 1)
    
    # Filtra los usuarios buscando estos campos:
    usuarios = User.objects.filter(
        Q(id__icontains=busqueda) |
        Q(username__icontains=busqueda) |
        Q(first_name__icontains=busqueda) |
        Q(last_name__icontains=busqueda) |
        Q(groups__name__icontains=busqueda)
    ).distinct()

    # Filtra el numero de usuarios de acuerdo al apartado "MOSTRAR"
    paginator = Paginator(usuarios, num_registros)
    usuarios_paginados = paginator.get_page(pagina)

    return render(request, 'menu-usuarios.html', {
        'usuarios': usuarios_paginados,
        'num_registros': num_registros,
        'busqueda': busqueda,
        'grupos': grupos
    })

@login_required
def buscar_usuarios(request):
    busqueda = request.GET.get('q', '')
    usuarios = User.objects.filter(
        Q(id__icontains=busqueda) |
        Q(username__icontains=busqueda) |
        Q(first_name__icontains=busqueda) |
        Q(last_name__icontains=busqueda) |
        Q(groups__name__icontains=busqueda)
    ).distinct()

    data = []
    for usuario in usuarios:
        grupos = [g.name for g in usuario.groups.all()]
        data.append({
            'id': usuario.id,
            'nombre': usuario.get_short_name(),
            'username': usuario.username,
            'grupos': ', '.join(grupos) if grupos else 'Sin grupo',
            'password': usuario.password[:15] + '...',
        })

    return JsonResponse({'usuarios': data})

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

def obtener_usuario(request, user_id):
    # Obtener el usuario por su ID
    user = get_object_or_404(User, id=user_id)
    # Retornar los datos del usuario en formato JSON
    return JsonResponse({
        "id": user.id,
        "nombre": user.first_name,
        "usuario": user.username,
        "grupo": [group.id for group in user.groups.all()],
    })

@require_POST
def actualizar_usuario(request):
    user_id = request.POST.get("user_id")
    user = get_object_or_404(User, id=user_id)

    user.first_name = request.POST.get("nombreEdit")
    user.username = request.POST.get("usuarioEdit")
    group_id = request.POST.get("grupoEdit")

    user.groups.clear()
    if group_id:
        group = get_object_or_404(Group, id=group_id)
        user.groups.add(group)
        
    # Cambia LA contraseña solo si se ingresó una nueva
    nueva_password = request.POST.get("passwordEdit")
    if nueva_password:
        user.set_password(nueva_password)

    user.save()
    referer = request.META.get('HTTP_REFERER', None)
    if referer:
        return redirect(referer)
    else:
        return redirect('lista-usuarios')