from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from .forms import FuncionarioForm
from .models import Funcionario
from treinamentos.models import Treinamento
from treinamentos.forms import TreinamentoForm

def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Funcionário cadastrado com sucesso!")
            return redirect('cadastrar_funcionario')
        else:
            messages.error(request, "Erro ao cadastrar. Verifique os campos!")
            print(form.errors)
    
    else:
        form = FuncionarioForm()

    return render(request, 'funcionarios/cadastro.html', {'form': form})

def listar_funcionarios(request):
    query = request.GET.get('q', '')
    ordenar_por = request.GET.get("ordenar_por", "id_funcionario")

    if ordenar_por == "nome":
        ordenacao = "nome_completo"
    elif ordenar_por == "-nome":
        ordenacao = "-nome_completo"
    else:
        ordenacao = "id_funcionario"

    funcionarios = Funcionario.objects.all().order_by(ordenacao)

    if query:
        funcionarios = funcionarios.filter(nome_completo__icontains=query)

    paginator = Paginator(funcionarios, 10)
    page = request.GET.get('page')
    funcionarios_paginados = paginator.get_page(page)

    return render(
        request,
        "funcionarios/listar.html",
        {
            "funcionarios": funcionarios_paginados,
            "query": query,
            "ordenar_por": ordenar_por,
        },
    )

def ficha_funcionario(request, id_funcionario): 
    funcionario = get_object_or_404(Funcionario, id_funcionario=id_funcionario)
    
    treinamentos = Treinamento.objects.filter(funcionario=funcionario).order_by('validade_passaporte')

    return render(request, "funcionarios/ficha.html", {
        "funcionario": funcionario,
        "treinamentos": treinamentos,
    })

def editar_funcionario(request, id_funcionario):
    funcionario = get_object_or_404(Funcionario, id_funcionario=id_funcionario)
    
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, request.FILES, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('ficha_funcionario', id_funcionario=funcionario.id_funcionario)
    else:
        form = FuncionarioForm(instance=funcionario)

    return render(request, 'funcionarios/editar.html', {'form': form, 'funcionario': funcionario})

def editar_treinamentos_funcionario(request, id_funcionario):
    funcionario = get_object_or_404(Funcionario, id_funcionario=id_funcionario)
    treinamentos = Treinamento.objects.filter(funcionario=funcionario)

    return render(request, 'treinamentos/editar_treinamentos.html', {
        'funcionario': funcionario,
        'treinamentos': treinamentos,
    })