from django.shortcuts import render
from django.http import HttpResponse

def cadastrar_treinamento(request):
    return render(request, "treinamentos/cadastrar.html")

def dashboard_treinamentos(request):
    return render(request, "treinamentos/dashboard.html")