from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.

def login(request): #First View
    context = {}  # Contexto vacío o con datos si los necesitas
    login_render = render_to_string('index.html', context)
    return HttpResponse(login_render)