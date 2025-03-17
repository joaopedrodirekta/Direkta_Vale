from django.db import models
from datetime import date
from funcionarios.models import Funcionario

# Lista de treinamentos disponíveis
TREINAMENTOS_CHOICES = [
    ("Disposições Gerais - PGR", "Disposições Gerais - PGR"),
    ("Equipamentos de Proteção Individual - EPI", "Equipamentos de Proteção Individual - EPI"),
    ("Segurança em Instalações e Serviços em Eletricidade", "Segurança em Instalações e Serviços em Eletricidade"),
    ("Transporte, Movimentação, Armazenagem e Manuseio", "Transporte, Movimentação, Armazenagem e Manuseio"),
    ("Segurança no Trabalho em Máquinas e Equipamentos", "Segurança no Trabalho em Máquinas e Equipamentos"),
    ("Ergonomia", "Ergonomia"),
    ("Segurança e Saúde no Trabalho na Indústria", "Segurança e Saúde no Trabalho na Indústria"),
    ("Trabalho em Altura", "Trabalho em Altura"),
    ("RAC - Trabalho em Altura", "RAC - Trabalho em Altura"),
    ("RAC - Veículos Automotores Leves", "RAC - Veículos Automotores Leves"),
    ("RAC - Operação de Equipamentos Móveis", "RAC - Operação de Equipamentos Móveis"),
    ("RAC - Bloqueio, Identificação e Zero Energia", "RAC - Bloqueio, Identificação e Zero Energia"),
    ("RAC - Içamento de Cargas", "RAC - Içamento de Cargas"),
    ("RAC - Proteção de Máquinas", "RAC - Proteção de Máquinas"),
    ("RAC - Trabalhos em Eletricidade", "RAC - Trabalhos em Eletricidade"),
    ("RAC - Trabalhos a Quente", "RAC - Trabalhos a Quente"),
    ("PRO - Trabalho em Altura", "PRO - Trabalho em Altura"),
    ("PRO - Operação de Veículos Leves", "PRO - Operação de Veículos Leves"),
    ("PRO - Operação com Equipamentos Móveis", "PRO - Operação com Equipamentos Móveis"),
    ("PRO - Bloqueio e Identificação", "PRO - Bloqueio e Identificação"),
    ("PRO - Içamento de Cargas", "PRO - Içamento de Cargas"),
    ("PRO - Proteção de Máquinas", "PRO - Proteção de Máquinas"),
    ("PRO - Trabalhos em Eletricidade", "PRO - Trabalhos em Eletricidade"),
    ("PRO - Isolamento de Área", "PRO - Isolamento de Área"),
    ("PRO - Ferramentas Manuais Rotativas", "PRO - Ferramentas Manuais Rotativas"),
    ("PRO - Trabalhos a Quente", "PRO - Trabalhos a Quente"),
    ("PGS - Regras de Ouro", "PGS - Regras de Ouro"),
    ("PGS - Prevenção de Fadiga", "PGS - Prevenção de Fadiga"),
    ("PGS - Grades de Piso", "PGS - Grades de Piso"),
    ("Treinamento Básico de SSMA", "Treinamento Básico de SSMA"),
    ("Ponte Rolante, Pórtico e Talha Elétrica", "Ponte Rolante, Pórtico e Talha Elétrica"),
    ("Sinaleiro/Amarrador de Cargas", "Sinaleiro/Amarrador de Cargas"),
    ("Brigadeiro Auxiliar de Emergência", "Brigadeiro Auxiliar de Emergência"),
    ("Ferramentas Abrasivas", "Ferramentas Abrasivas"),
    ("Treinamento Montagem/Desmontagem Andaime", "Treinamento Montagem/Desmontagem Andaime"),
    ("Operação Plataforma Trabalho Aéreo", "Operação Plataforma Trabalho Aéreo"),
    ("Operações de Soldagem e Corte a Quente", "Operações de Soldagem e Corte a Quente"),
    ("Uso de Máquina de Solda", "Uso de Máquina de Solda"),
    ("Inspeção de Acessórios de Içamento de Cargas", "Inspeção de Acessórios de Içamento de Cargas"),
    ("Operador de Guindaste Veicular (Caminhão Munck)", "Operador de Guindaste Veicular (Caminhão Munck)"),
    ("PTS - Executante Credenciado", "PTS - Executante Credenciado"),
    ("PTS - Emitente", "PTS - Emitente"),
    ("ART - Análise de Risco da Tarefa", "ART - Análise de Risco da Tarefa"),
    ("Noções de Primeiros Socorros", "Noções de Primeiros Socorros"),
    ("Operador de Plataformas Elevatórias", "Operador de Plataformas Elevatórias"),
]

# Mapeamento do treinamento para a norma correspondente
NORMAS = {
    treinamento[0]: norma for treinamento, norma in zip(TREINAMENTOS_CHOICES, [
        "NR 01", "NR 06", "NR 10", "NR 11", "NR 12", "NR 17", "NR 18", "NR 35",
        "RAC 01", "RAC 02", "RAC 03", "RAC 04", "RAC 05", "RAC 07", "RAC 10", "RAC 12",
        "PRO RAC 01", "PRO RAC 02", "PRO RAC 03", "PRO RAC 04", "PRO RAC 05", "PRO RAC 07",
        "PRO RAC 10", "PRO - 006218", "PRO - 015971", "PRO - 025676", "PGS - 003632",
        "PGS - 004633", "PGS - 004728", "TBSSMA", "--", "NR 18", "--", "NR 12",
        "NR 18", "--", "NR 18", "--", "NR 11", "--", "--", "--", "--", "NR 11", "--",
    ])
}

class Treinamento(models.Model):
    funcionario = models.ForeignKey(
        Funcionario, on_delete=models.CASCADE, verbose_name="Funcionário"
    )  # Obrigatório
    nome_treinamento = models.CharField(
        max_length=255, choices=TREINAMENTOS_CHOICES, verbose_name="Nome do Treinamento"
    )  # Obrigatório
    norma = models.CharField(max_length=50, verbose_name="Norma")  # Obrigatório
    carga_horaria = models.TimeField(blank=True, null=True, verbose_name="Carga Horária")  # Opcional
    data_inicio = models.DateField(blank=True, null=True, verbose_name="Data de Início")  # Opcional
    data_fim = models.DateField(blank=True, null=True, verbose_name="Data de Fim")  # Opcional
    validade_certificado = models.DateField(blank=True, null=True, verbose_name="Validade do Certificado")  # Opcional
    validade_passaporte = models.DateField(blank=True, null=True, verbose_name="Validade do Passaporte")  # Opcional

    class Meta:
        verbose_name = "Treinamento"
        verbose_name_plural = "Treinamentos"
        ordering = ["nome_treinamento"]

    def calcular_status(self):
        """Calcula os dias restantes para o vencimento e retorna um status formatado"""
        hoje = date.today()

        # Verifica se a validade do passaporte está em branco
        if not self.validade_passaporte:
            return "Sem Validade", "cinza"

        dias_restantes = (self.validade_passaporte - hoje).days

        if dias_restantes > 30:
            return f"Faltam {dias_restantes} dias", "verde"
        elif 15 <= dias_restantes <= 29:
            return f"Faltam {dias_restantes} dias", "azul"
        elif 1 <= dias_restantes <= 14:
            return f"Faltam {dias_restantes} dias", "amarelo"
        else:
            return "VENCIDO", "vermelho"

    def save(self, *args, **kwargs):
        """Ao salvar, define automaticamente a norma com base no treinamento"""
        if self.nome_treinamento in NORMAS:
            self.norma = NORMAS[self.nome_treinamento]
        super().save(*args, **kwargs)

    def __str__(self):
        """Evita erro ao acessar o nome do funcionário se ele não estiver vinculado"""
        return f"{self.funcionario.nome_completo} - {self.nome_treinamento}" if self.funcionario else self.nome_treinamento