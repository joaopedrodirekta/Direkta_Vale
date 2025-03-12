from django.shortcuts import render, redirect, get_object_or_404
from .forms import FuncionarioForm
from django.contrib import messages
from .models import Funcionario

def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Funcionário cadastrado com sucesso!")
            return redirect('listar_funcionarios')
    else:
        print(form.errors)  # Exibir erros no terminal para depuração

    return render(request, 'funcionarios/cadastro.html', {'form': form})

# Lista todos os funcionários
def listar_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, "funcionarios/listar.html", {"funcionarios": funcionarios})

# Exibe a ficha de um funcionário específico
def ficha_funcionario(request, id_funcionario):
    funcionario = get_object_or_404(Funcionario, id_funcionario=id_funcionario)
    return render(request, "funcionarios/ficha.html", {"funcionario": funcionario})