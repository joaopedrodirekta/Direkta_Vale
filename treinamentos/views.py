from django.shortcuts import render, redirect
from .forms import TreinamentoForm
from .models import Treinamento, TREINAMENTOS_CHOICES, NORMAS
from funcionarios.models import Funcionario

def cadastrar_treinamento(request):
    funcionarios = Funcionario.objects.all()  # Garantir que há funcionários cadastrados
    treinamentos = [treinamento[0] for treinamento in TREINAMENTOS_CHOICES]  # Extraindo apenas os nomes dos treinamentos

    if request.method == "POST":
        form = TreinamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_treinamentos")  # Redireciona após salvar
    else:
        form = TreinamentoForm()

    return render(request, "treinamentos/cadastro.html", {
        "form": form,
        "funcionarios": funcionarios,
        "treinamentos": treinamentos,
        "normas": NORMAS
    })

def dashboard_treinamentos(request):
    return render(request, "treinamentos/dashboard.html")