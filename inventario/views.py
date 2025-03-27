from django.shortcuts import render
from django.http import HttpResponse

def inventario_home(request):
    return render(request, 'inventario/home.html')

def cadastrar_item(request):
    return render(request, 'inventario/cadastro.html')

def listar_inventario(request):
    return render(request, 'inventario/listar.html')

def imprimir_lista(request):
    return render(request, 'inventario/imprimir.html')
