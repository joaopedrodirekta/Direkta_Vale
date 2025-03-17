from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import TreinamentoForm
from .models import Treinamento, TREINAMENTOS_CHOICES, NORMAS
from funcionarios.models import Funcionario

def cadastrar_treinamento(request):
    funcionarios = Funcionario.objects.all()
    treinamentos = [treinamento[0] for treinamento in TREINAMENTOS_CHOICES]

    if request.method == "POST":
        form = TreinamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard_treinamentos")  # Redireciona para o dashboard
        else:
            print(form.errors)  # Exibe os erros no terminal
    else:
        form = TreinamentoForm()

    return render(request, "treinamentos/cadastro.html", {
        "form": form,
        "funcionarios": funcionarios,
        "treinamentos": treinamentos,
        "normas": NORMAS
    })

def dashboard_treinamentos(request):
    treinamentos = Treinamento.objects.all()

    # Contadores de status
    total_treinamentos = treinamentos.count()
    vencidos = sum(1 for t in treinamentos if t.calcular_status()[1] == "vermelho")
    alerta = sum(1 for t in treinamentos if t.calcular_status()[1] == "amarelo")
    atencao = sum(1 for t in treinamentos if t.calcular_status()[1] == "azul")
    ok = sum(1 for t in treinamentos if t.calcular_status()[1] == "verde")
    sem_validade = sum(1 for t in treinamentos if t.calcular_status()[1] == "cinza")

    context = {
        "total_treinamentos": total_treinamentos,
        "vencidos": vencidos,
        "alerta": alerta,
        "atencao": atencao,
        "ok": ok,
        "sem_validade": sem_validade,
    }

    return render(request, "treinamentos/dashboard.html", context)