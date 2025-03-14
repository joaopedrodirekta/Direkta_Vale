from django import forms
from .models import Treinamento, TREINAMENTOS_CHOICES
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
    )

    class Meta:
        model = Treinamento
        fields = [
            "funcionario",
            "nome_treinamento",
            "carga_horaria",
            "data_inicio",
            "data_fim",
            "validade_certificado",
            "validade_passaporte",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nome_treinamento"].widget.attrs["onchange"] = "atualizarNorma()"
        self.fields["funcionario"].widget.attrs["onchange"] = "atualizarDadosFuncionario()"