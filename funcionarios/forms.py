from django import forms
from .models import Funcionario
from datetime import date
from django.core.exceptions import ValidationError
import re

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'rg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o RG'}),
            'contato_pessoal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular'}),
            'contato_emergencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contato de emergência'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'validade_cnh': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_admissao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_mobilizacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_desligamento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_desmobilizacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_cpf(self):
        """Valida o formato do CPF"""
        cpf = self.cleaned_data.get('cpf')
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            raise ValidationError("O CPF deve estar no formato 000.000.000-00")
        return cpf

    def clean_data_nascimento(self):
        """Impede que a data de nascimento seja no futuro"""
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento and data_nascimento > date.today():
            raise ValidationError("A data de nascimento não pode ser no futuro.")
        return data_nascimento