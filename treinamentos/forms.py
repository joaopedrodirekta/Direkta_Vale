from django import forms
from .models import Treinamento
from funcionarios.models import Funcionario

class TreinamentoForm(forms.ModelForm):
    funcionario_nome = forms.ModelChoiceField(
        queryset=Funcionario.objects.all(),
        label="Funcionário",
        empty_label="Selecione um funcionário",
    )

    class Meta:
        model = Treinamento
        fields = [
            "funcionario_nome",
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