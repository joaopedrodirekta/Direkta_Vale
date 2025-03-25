from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from .forms import FuncionarioForm
from .models import Funcionario

def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Funcionário cadastrado com sucesso!")
            return redirect('cadastrar_funcionario')
        else:
            messages.error(request, "Erro ao cadastrar. Verifique os campos!")
            print(form.errors)  # Adiciona logs dos erros no terminal do Render
    
    else:
        form = FuncionarioForm()

    return render(request, 'funcionarios/cadastro.html', {'form': form})

def listar_funcionarios(request):
    query = request.GET.get('q')
    funcionarios = Funcionario.objects.all().order_by('-data_admissao')

    if query:
        funcionarios = funcionarios.filter(nome_completo__icontains=query)

    paginator = Paginator(funcionarios, 10)  # Paginação com 10 funcionários por página
    page = request.GET.get('page')
    funcionarios_paginados = paginator.get_page(page)
    ordenar_por = request.GET.get("ordenar_por", "id_funcionario")

    if ordenar_por == "nome":
        funcionarios = Funcionario.objects.all().order_by("nome_completo")
    elif ordenar_por == "-nome":
        funcionarios = Funcionario.objects.all().order_by("-nome_completo")
    else:
        funcionarios = Funcionario.objects.all().order_by("id_funcionario")

    return render(request, "funcionarios/listar.html", {"funcionarios": funcionarios_paginados, "query": query})

def ficha_funcionario(request, id_funcionario):
    funcionario = get_object_or_404(Funcionario, id_funcionario=id_funcionario)
    return render(request, "funcionarios/ficha.html", {"funcionario": funcionario})

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