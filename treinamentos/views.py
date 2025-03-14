from django.shortcuts import render, redirect
from .forms import TreinamentoForm

def cadastrar_treinamento(request):
    if request.method == "POST":
        form = TreinamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_treinamentos")  # Redireciona após salvar
    else:
        form = TreinamentoForm()

    return render(request, "treinamentos/cadastro.html", {"form": form})

def dashboard_treinamentos(request):
    return render(request, "treinamentos/dashboard.html")