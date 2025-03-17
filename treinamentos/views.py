from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date, timedelta
from .forms import TreinamentoForm
from .models import Treinamento, TREINAMENTOS_CHOICES, NORMAS
from funcionarios.models import Funcionario

def cadastrar_treinamento(request):
    funcionarios = Funcionario.objects.all()  
    treinamentos = [treinamento[0] for treinamento in TREINAMENTOS_CHOICES]  

    if request.method == "POST":
        form = TreinamentoForm(request.POST)
        if form.is_valid():
            treinamento = form.save(commit=False)

            # Definir automaticamente a norma antes de salvar
            treinamento.norma = NORMAS.get(treinamento.nome_treinamento, "")

            treinamento.save()
            messages.success(request, "Treinamento cadastrado com sucesso!")
            return redirect("dashboard_treinamentos")  # Redireciona para o dashboard
        else:
            messages.error(request, "Erro ao cadastrar treinamento. Verifique os campos obrigatórios.")
            print(form.errors)  # Para depuração no terminal

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
    vencidos = treinamentos.filter(validade_passaporte__lte=date.today()).count()
    alerta = treinamentos.filter(validade_passaporte__gt=date.today(), validade_passaporte__lte=date.today() + timedelta(days=14)).count()
    atencao = treinamentos.filter(validade_passaporte__gt=date.today() + timedelta(days=14), validade_passaporte__lte=date.today() + timedelta(days=29)).count()
    ok = treinamentos.filter(validade_passaporte__gt=date.today() + timedelta(days=30)).count()
    sem_validade = treinamentos.filter(validade_passaporte__isnull=True).count()

    context = {
        "total_treinamentos": total_treinamentos,
        "vencidos": vencidos,
        "alerta": alerta,
        "atencao": atencao,
        "ok": ok,
        "sem_validade": sem_validade,
    }

    return render(request, "treinamentos/dashboard.html", context)