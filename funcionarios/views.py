from django.shortcuts import render, redirect
from .forms import FuncionarioForm
from django.contrib import messages

def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Funcionário cadastrado com sucesso!")
            return redirect('cadastrar_funcionario')
    else:
        form = FuncionarioForm()

    return render(request, 'funcionarios/cadastro.html', {'form': form})

def listar_funcionarios(request):
    return render(request, "funcionarios/listar.html")