"""
URL configuration for SIPRE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login.views import login, cerrar_sesion, menu_admin, menu_finanzas, menu_contabilidad, menu_general, submenu_presupuestos_1
from usuarios.views import lista_usuarios, eliminar_usuarios, registrar_usuario, obtener_usuario, actualizar_usuario, buscar_usuarios

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('menu_admin/', menu_admin, name='menu-admin'),
    path('menu_finanzas/', menu_finanzas, name='menu-finanzas'),
    path('menu_contabilidad/', menu_contabilidad, name='menu-contabilidad'),
    path('menu_general/', menu_general, name='menu-general'),
    path('usuarios/', lista_usuarios, name='lista-usuarios'),
    path('usuarios/eliminar-multiples/', eliminar_usuarios, name='eliminar-usuarios'),
    path('usuarios/registrar/', registrar_usuario, name='registrar-usuario'),
    path('usuarios/obtener/<int:user_id>/', obtener_usuario, name='obtener-usuario'),
    path('usuarios/actualizar/', actualizar_usuario, name='actualizar-usuario'),
    path('usuarios/buscar/', buscar_usuarios, name='buscar-usuarios'),
    path('submenu_pre_1/', submenu_presupuestos_1, name='submenu-pre-1')
]
