from django import forms
from .models import Treinamento, TREINAMENTOS_CHOICES, NORMAS
from funcionarios.models import Funcionario

class TreinamentoForm(forms.ModelForm):
    funcionario = forms.ModelChoiceField(
        queryset=Funcionario.objects.all(),
        label="Nome do Funcionário",
        empty_label="Selecione...",
    )

    nome_treinamento = forms.ChoiceField(
        choices=TREINAMENTOS_CHOICES,
        label="Nome do Treinamento",
        required=True
    )

    norma = forms.CharField(
        label="Norma",
        required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    carga_horaria = forms.TimeField(
        label="Carga Horária (HH:MM)",
        required=False,
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'})
    )

    data_inicio = forms.DateField(
        label="Data Inicial",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    data_fim = forms.DateField(
        label="Data Final",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    validade_certificado = forms.DateField(
        label="Validade do Certificado",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    validade_passaporte = forms.DateField(
        label="Validade Passaporte - Vale",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Treinamento
        fields = [
            "funcionario",
            "nome_treinamento",
            "norma",
            "carga_horaria",
            "data_inicio",
            "data_fim",
            "validade_certificado",
            "validade_passaporte",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Preencher automaticamente a norma baseada no treinamento selecionado
        self.fields["nome_treinamento"].widget.attrs["onchange"] = "atualizarNorma()"
        self.fields["funcionario"].widget.attrs["onchange"] = "atualizarDadosFuncionario()"