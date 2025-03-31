# ========================
# IMPORTS
# ========================
import calendar
import pandas as pd

from datetime import date, timedelta
from collections import defaultdict
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .forms import TreinamentoForm
from .models import Treinamento, TREINAMENTOS_CHOICES, NORMAS
from funcionarios.models import Funcionario

# ========================
# CADASTRO DE TREINAMENTO
# ========================

def cadastrar_treinamento(request):
    funcionarios = Funcionario.objects.all()
    treinamentos = [treinamento[0] for treinamento in TREINAMENTOS_CHOICES]

    if request.method == "POST":
        form = TreinamentoForm(request.POST)
        if form.is_valid():
            treinamento = form.save(commit=False)
            funcionario_id = request.POST.get("funcionario")

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

            treinamento.norma = NORMAS.get(treinamento.nome_treinamento, "")
            treinamento.save()
            messages.success(request, "Treinamento cadastrado com sucesso!")
            form = TreinamentoForm()
        else:
            messages.error(request, "Erro ao cadastrar treinamento.")
            print(form.errors)
    else:
        form = TreinamentoForm()

    return render(request, "treinamentos/cadastro.html", {
        "form": form,
        "funcionarios": funcionarios,
        "treinamentos": treinamentos,
        "normas": NORMAS
    })

# ========================
# DASHBOARD
# ========================

def dashboard_treinamentos(request):
    treinamentos = Treinamento.objects.select_related('funcionario').all()
    today = timezone.now().date()

    total_treinamentos = treinamentos.count()
    vencidos = treinamentos.filter(validade_passaporte__lte=today).count()
    alerta = treinamentos.filter(validade_passaporte__gt=today, validade_passaporte__lte=today + timedelta(days=14)).count()
    atencao = treinamentos.filter(validade_passaporte__gt=today + timedelta(days=15), validade_passaporte__lte=today + timedelta(days=29)).count()
    ok = treinamentos.filter(validade_passaporte__gt=today + timedelta(days=30)).count()
    sem_validade = treinamentos.filter(validade_passaporte__isnull=True).count()

    treinamentos_vencendo = treinamentos.filter(validade_passaporte__gt=today)
    treinamentos_por_mes = defaultdict(int)

    for t in treinamentos_vencendo:
        if t.validade_passaporte:
            mes = t.validade_passaporte.strftime("%Y-%m")
            treinamentos_por_mes[mes] += 1

    treinamentos_por_mes = {
        calendar.month_name[int(m.split("-")[1])]: treinamentos_por_mes[m]
        for m in sorted(treinamentos_por_mes)
    }

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
        "today": today,
        "treinamentos_por_mes": treinamentos_por_mes,
    }
    return render(request, "treinamentos/dashboard.html", context)

# ========================
# EXPORTAR DADOS
# ========================

def exportar_excel(request):
    treinamentos = Treinamento.objects.select_related('funcionario').all()
    today = date.today()

    dados = []
    for treinamento in treinamentos:
        validade = treinamento.validade_passaporte
        if validade:
            dias_restantes = (validade - today).days
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
            "Data de Vencimento": validade.strftime("%d/%m/%Y") if validade else "-",
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

    y = height - 80
    col_titles = ["ID Func.", "Nome", "Treinamento", "Norma", "Vencimento", "Status"]
    x_positions = [40, 100, 250, 400, 500, 580]

    pdf.setFont("Helvetica-Bold", 10)
    for i, title in enumerate(col_titles):
        pdf.drawString(x_positions[i], y, title)

    pdf.line(30, y - 5, 580, y - 5)
    pdf.setFont("Helvetica", 9)
    y -= 20

    for t in treinamentos:
        validade = t.validade_passaporte
        if validade:
            dias_restantes = (validade - today).days
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

        pdf.drawString(x_positions[0], y, t.funcionario.id_funcionario)
        pdf.drawString(x_positions[1], y, t.funcionario.nome_completo[:22])
        pdf.drawString(x_positions[2], y, t.nome_treinamento[:30])
        pdf.drawString(x_positions[3], y, t.norma)
        pdf.drawString(x_positions[4], y, validade.strftime("%d/%m/%Y") if validade else "-")
        pdf.drawString(x_positions[5], y, status_label)

        y -= 20
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 9)
            y = height - 50

    pdf.save()
    return response

# ========================
# ATUALIZAR / EXCLUIR
# ========================

def atualizar_treinamento(request, treinamento_id):
    treinamento = get_object_or_404(Treinamento, id=treinamento_id)
    funcionario = treinamento.funcionario

    if request.method == "POST":
        treinamento.data_inicio = request.POST.get("data_inicio") or None
        treinamento.data_fim = request.POST.get("data_fim") or None
        treinamento.carga_horaria = request.POST.get("carga_horaria") or None
        treinamento.validade_certificado = request.POST.get("validade_certificado") or None
        treinamento.validade_passaporte = request.POST.get("validade_passaporte") or None
        treinamento.save()

        messages.success(request, "Treinamento atualizado com sucesso!")
        return redirect("dashboard_treinamentos")

    return render(request, 'treinamentos/atualizar_treinamento.html', {
        'treinamento': treinamento,
        'funcionario': funcionario
    })

@require_POST
def atualizar_treinamento_ajax(request):
    try:
        data = request.POST
        treinamento = Treinamento.objects.get(id=data.get("id"))
        treinamento.data_inicio = data.get("data_inicio") or None
        treinamento.data_fim = data.get("data_fim") or None
        treinamento.carga_horaria = data.get("carga_horaria") or None
        treinamento.validade_certificado = data.get("validade_certificado") or None
        treinamento.validade_passaporte = data.get("validade_passaporte") or None
        treinamento.save()
        return JsonResponse({"status": "ok"})
    except Treinamento.DoesNotExist:
        return JsonResponse({"status": "erro", "mensagem": "Treinamento não encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"status": "erro", "mensagem": str(e)}, status=400)

def excluir_treinamento(request, treinamento_id):
    treinamento = get_object_or_404(Treinamento, id=treinamento_id)
    if request.method == 'POST':
        treinamento.delete()
        messages.success(request, "Treinamento excluído com sucesso!")
    return redirect('dashboard_treinamentos')

# ========================
# LISTAGEM E EDIÇÃO
# ========================

def listar_treinamentos(request):
    treinamentos = Treinamento.objects.select_related('funcionario').all()
    today = timezone.now().date()

    nome_funcionario = request.GET.get('nome_funcionario', '')
    nome_treinamento = request.GET.get('nome_treinamento', '')
    status = request.GET.get('status', '')

    if nome_funcionario:
        treinamentos = treinamentos.filter(funcionario__nome_completo__icontains=nome_funcionario)
    if nome_treinamento:
        treinamentos = treinamentos.filter(nome_treinamento__icontains=nome_treinamento)
    if status:
        treinamentos = treinamentos.filter(status=status)

    ordenar_por = request.GET.get('ordenar_por')
    if ordenar_por == 'funcionario':
        treinamentos = treinamentos.order_by('funcionario__nome_completo')
    elif ordenar_por == 'treinamento':
        treinamentos = treinamentos.order_by('nome_treinamento')

    for t in treinamentos:
        if t.validade_passaporte:
            dias = (t.validade_passaporte - today).days
            if dias < 0:
                t.status_label = "Vencido"
                t.status_class = "bg-danger text-white"
            elif dias <= 14:
                t.status_label = "Urgente"
                t.status_class = "bg-warning text-dark"
            elif dias <= 29:
                t.status_label = "Atenção"
                t.status_class = "bg-primary text-white"
            else:
                t.status_label = "Válido"
                t.status_class = "bg-success text-white"
        else:
            t.status_label = "Sem Validade"
            t.status_class = "bg-secondary text-white"

    return render(request, 'treinamentos/listar_treinamentos.html', {
        'treinamentos': treinamentos,
        'nome_funcionario': nome_funcionario,
        'nome_treinamento': nome_treinamento,
        'status': status,
        'ordenar_por': ordenar_por,
    })

def editar_treinamentos_funcionario(request, id_funcionario):
    funcionario = get_object_or_404(Funcionario, id_funcionario=id_funcionario)
    treinamentos = Treinamento.objects.filter(funcionario=funcionario)

    return render(request, 'treinamentos/editar_treinamentos.html', {
        'funcionario': funcionario,
        'treinamentos': treinamentos,
    })