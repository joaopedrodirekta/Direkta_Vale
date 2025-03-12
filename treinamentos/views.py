from django.shortcuts import render
from django.http import HttpResponse

def lista_treinamentos(request):
    return HttpResponse("Página de Treinamentos")