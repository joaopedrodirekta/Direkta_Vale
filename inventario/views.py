from django.shortcuts import render
from django.http import HttpResponse

def lista_itens(request):
    return HttpResponse("Página de Inventário")