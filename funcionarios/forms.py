from django import forms
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'validade_cnh': forms.DateInput(attrs={'type': 'date'}),
            'data_admissao': forms.DateInput(attrs={'type': 'date'}),
            'data_mobilizacao': forms.DateInput(attrs={'type': 'date'}),
            'data_desligamento': forms.DateInput(attrs={'type': 'date'}),
            'data_desmobilizacao': forms.DateInput(attrs={'type': 'date'}),
        }