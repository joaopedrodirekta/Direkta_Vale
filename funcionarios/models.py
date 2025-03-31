from django.db import models
from datetime import date
import os
from uuid import uuid4
import re
from django.core.exceptions import ValidationError

def upload_funcionario(instance, filename):
    """Gera um nome único para a foto do funcionário."""
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('fotos_funcionarios/', filename)

def validar_cpf(value):
    """Valida o formato do CPF."""
    if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', value):
        raise ValidationError("O CPF deve estar no formato 000.000.000-00")

class Funcionario(models.Model):
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')]
    STATUS_CHOICES = [('Contratado', 'Contratado'), ('Desligado', 'Desligado')]

    id_funcionario = models.CharField(max_length=20, primary_key=True, unique=True)
    foto = models.ImageField(upload_to=upload_funcionario, blank=True, null=True)
    
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True, validators=[validar_cpf], db_index=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    sexo = models.CharField(max_length=20, choices=SEXO_CHOICES, default='M')
    data_nascimento = models.DateField()
    cnh = models.CharField(max_length=20, blank=True, null=True)
    validade_cnh = models.DateField(blank=True, null=True)
    contato_pessoal = models.CharField(max_length=20, blank=True, null=True)
    contato_emergencia = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, db_index=True, blank=True, null=True)

    funcao = models.CharField(max_length=100, db_index=True)
    departamento = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Contratado')
    data_admissao = models.DateField()
    data_mobilizacao = models.DateField(blank=True, null=True)
    data_desligamento = models.DateField(blank=True, null=True)
    data_desmobilizacao = models.DateField(blank=True, null=True)
    cracha_vale = models.CharField(max_length=50, blank=True, null=True)

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    @property
    def idade(self):
        """Retorna a idade do funcionário."""
        today = date.today()
        return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))

    class Meta:
        db_table = 'funcionarios'

    def __str__(self):
        return f"{self.id_funcionario} - {self.nome_completo}"