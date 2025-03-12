from django.shortcuts import render
from django.http import HttpResponse

def lista_funcionarios(request):
    return HttpResponse("Página de Funcionários")