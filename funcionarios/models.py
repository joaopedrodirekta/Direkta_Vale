from django.db import models
from datetime import date

class Funcionario(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('Contratado', 'Contratado'),
        ('Desligado', 'Desligado'),
    ]

    # ID do Funcionário (Agora será inserido manualmente)
    id_funcionario = models.CharField(max_length=10, primary_key=True, unique=True)

    # Foto
    foto = models.ImageField(upload_to='fotos_funcionarios/', blank=True, null=True)

    # Dados Pessoais
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default='M')
    data_nascimento = models.DateField()
    cnh = models.CharField(max_length=20, blank=True, null=True)
    validade_cnh = models.DateField(blank=True, null=True)
    contato_pessoal = models.CharField(max_length=20)
    contato_emergencia = models.CharField(max_length=20)
    email = models.EmailField()

    # Dados Profissionais
    funcao = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Contratado')
    data_admissao = models.DateField()
    data_mobilizacao = models.DateField(blank=True, null=True)
    data_desligamento = models.DateField(blank=True, null=True)
    data_desmobilizacao = models.DateField(blank=True, null=True)
    cracha_vale = models.CharField(max_length=50, blank=True, null=True)

    def calcular_idade(self):
        """Calcula a idade automaticamente com base na data de nascimento."""
        today = date.today()
        return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))

    def __str__(self):
        return f"{self.id_funcionario} - {self.nome_completo}"