from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date, timedelta
from .forms import TreinamentoForm
from .models import Treinamento, TREINAMENTOS_CHOICES, NORMAS
from funcionarios.models import Funcionario
from django.utils import timezone
import pandas as pd
from django.http import HttpResponse
from django.http import FileResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def cadastrar_treinamento(request):
    funcionarios = Funcionario.objects.all()  
    treinamentos = [treinamento[0] for treinamento in TREINAMENTOS_CHOICES]  

    if request.method == "POST":
        form = TreinamentoForm(request.POST)
        if form.is_valid():
            treinamento = form.save(commit=False)
            funcionario_id = request.POST.get("funcionario")  # Captura corretamente o ID do funcionário

            try:
                treinamento.funcionario = Funcionario.objects.get(id_funcionario=funcionario_id)
            except Funcionario.DoesNotExist:
                messages.error(request, "Funcionário não encontrado.")
                return render(request, "treinamentos/cadastro.html", {
                    "form": form,
                    "funcionarios": funcionarios,
                    "treinamentos": treinamentos,
                    "normas": NORMAS
                })

            # Define automaticamente a norma antes de salvar
            treinamento.norma = NORMAS.get(treinamento.nome_treinamento, "")
            treinamento.save()
            
            messages.success(request, "Treinamento cadastrado com sucesso!")
            form = TreinamentoForm()  # Reinicia o formulário para um novo cadastro
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
    treinamentos = Treinamento.objects.select_related('funcionario').all()
    today = timezone.now().date()  # Garante que está usando a data correta

    total_treinamentos = treinamentos.count()
    vencidos = treinamentos.filter(validade_passaporte__lte=date.today()).count()
    alerta = treinamentos.filter(validade_passaporte__gt=date.today(), validade_passaporte__lte=date.today() + timedelta(days=14)).count()
    atencao = treinamentos.filter(validade_passaporte__gt=date.today() + timedelta(days=15), validade_passaporte__lte=date.today() + timedelta(days=29)).count()
    ok = treinamentos.filter(validade_passaporte__gt=date.today() + timedelta(days=30)).count()
    sem_validade = treinamentos.filter(validade_passaporte__isnull=True).count()

    for treinamento in treinamentos:
        if treinamento.validade_passaporte:
            dias_restantes = (treinamento.validade_passaporte - today).days
            if dias_restantes < 0:
                treinamento.status_label = "Vencido"
                treinamento.status_class = "bg-danger"
            elif dias_restantes <= 14:
                treinamento.status_label = "Urgente"
                treinamento.status_class = "bg-warning"
            elif dias_restantes <= 29:
                treinamento.status_label = "Atenção"
                treinamento.status_class = "bg-primary"
            else:
                treinamento.status_label = "Válido"
                treinamento.status_class = "bg-success"
        else:
            treinamento.status_label = "Sem Validade"
            treinamento.status_class = "bg-secondary"

    context = {
        "total_treinamentos": total_treinamentos,
        "vencidos": vencidos,
        "alerta": alerta,
        "atencao": atencao,
        "ok": ok,
        "sem_validade": sem_validade,
        "treinamentos": treinamentos,
        "today": today,  # Passar a data atual para uso no template
    }

    return render(request, "treinamentos/dashboard.html", context)

def exportar_excel(request):
    treinamentos = Treinamento.objects.select_related('funcionario').all()
    today = date.today()

    dados = []
    for treinamento in treinamentos:
        # Recriando a lógica de status_label
        if treinamento.validade_passaporte:
            dias_restantes = (treinamento.validade_passaporte - today).days
            if dias_restantes < 0:
                status_label = "Vencido"
            elif dias_restantes <= 14:
                status_label = "Urgente"
            elif dias_restantes <= 29:
                status_label = "Atenção"
            else:
                status_label = "Válido"
        else:
            status_label = "Sem Validade"

        dados.append({
            "ID Funcionário": treinamento.funcionario.id_funcionario,
            "Nome": treinamento.funcionario.nome_completo,
            "Treinamento": treinamento.nome_treinamento,
            "Norma": treinamento.norma,
            "Data de Vencimento": treinamento.validade_passaporte.strftime("%d/%m/%Y") if treinamento.validade_passaporte else "-",
            "Status": status_label
        })

    df = pd.DataFrame(dados)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="treinamentos.xlsx"'
    df.to_excel(response, index=False)

    return response

def exportar_pdf(request):
    treinamentos = Treinamento.objects.select_related('funcionario').all()
    today = date.today()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="treinamentos.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, height - 40, "Relatório de Treinamentos")

    pdf.setFont("Helvetica-Bold", 10)
    y = height - 80  

    col_titles = ["ID Func.", "Nome", "Treinamento", "Norma", "Vencimento", "Status"]
    x_positions = [40, 100, 250, 400, 500, 580]  

    for i, title in enumerate(col_titles):
        pdf.drawString(x_positions[i], y, title)

    pdf.line(30, y - 5, 580, y - 5)  
    pdf.setFont("Helvetica", 9)
    y -= 20  

    for treinamento in treinamentos:
        # Recriando a lógica de status_label
        if treinamento.validade_passaporte:
            dias_restantes = (treinamento.validade_passaporte - today).days
            if dias_restantes < 0:
                status_label = "Vencido"
            elif dias_restantes <= 14:
                status_label = "Urgente"
            elif dias_restantes <= 29:
                status_label = "Atenção"
            else:
                status_label = "Válido"
        else:
            status_label = "Sem Validade"

        pdf.drawString(x_positions[0], y, treinamento.funcionario.id_funcionario)
        pdf.drawString(x_positions[1], y, treinamento.funcionario.nome_completo[:22])  
        pdf.drawString(x_positions[2], y, treinamento.nome_treinamento[:30])  
        pdf.drawString(x_positions[3], y, treinamento.norma)
        pdf.drawString(x_positions[4], y, treinamento.validade_passaporte.strftime("%d/%m/%Y") if treinamento.validade_passaporte else "-")
        pdf.drawString(x_positions[5], y, status_label)

        y -= 20  
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 9)
            y = height - 50

    pdf.save()
    return response