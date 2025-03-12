from django.shortcuts import render
from django.http import HttpResponse

def cadastrar_funcionario(request):
    return render(request, "funcionarios/cadastrar.html")

def listar_funcionarios(request):
    return render(request, "funcionarios/listar.html")