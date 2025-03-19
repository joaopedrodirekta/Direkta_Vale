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

    # Criar um DataFrame com os dados necessários
    data = {
        "ID Funcionário": [t.funcionario.id_funcionario for t in treinamentos],
        "Nome": [t.funcionario.nome_completo for t in treinamentos],
        "Treinamento": [t.nome_treinamento for t in treinamentos],
        "Norma": [t.norma for t in treinamentos],
        "Data de Vencimento": [t.validade_passaporte.strftime('%d/%m/%Y') if t.validade_passaporte else "-" for t in treinamentos],
        "Status": [t.status_label for t in treinamentos]
    }

    df = pd.DataFrame(data)

    # Criar a resposta HTTP com o arquivo Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="treinamentos.xlsx"'

    # Salvar o DataFrame no Excel e enviar a resposta
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name="Treinamentos", index=False)

    return response

def exportar_pdf(request):
    treinamentos = Treinamento.objects.select_related('funcionario').all()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40  # Posição inicial no PDF

    # Título
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, y, "Relatório de Treinamentos")
    y -= 30

    # Cabeçalhos
    pdf.setFont("Helvetica-Bold", 10)
    colunas = ["ID", "Nome", "Treinamento", "Norma", "Vencimento", "Status"]
    x_positions = [30, 80, 200, 400, 500, 570]  # Posições das colunas

    for i, coluna in enumerate(colunas):
        pdf.drawString(x_positions[i], y, coluna)

    pdf.setFont("Helvetica", 10)
    y -= 20

    # Dados da tabela
    for t in treinamentos:
        pdf.drawString(x_positions[0], y, str(t.funcionario.id_funcionario))
        pdf.drawString(x_positions[1], y, t.funcionario.nome_completo[:20])  # Limita nome a 20 caracteres
        pdf.drawString(x_positions[2], y, t.nome_treinamento[:30])  # Limita o treinamento a 30 caracteres
        pdf.drawString(x_positions[3], y, t.norma)
        pdf.drawString(x_positions[4], y, t.validade_passaporte.strftime('%d/%m/%Y') if t.validade_passaporte else "-")
        pdf.drawString(x_positions[5], y, t.status_label)
        y -= 20  # Move para a próxima linha

        if y < 40:  # Adiciona nova página se necessário
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = height - 40

    pdf.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="treinamentos.pdf")