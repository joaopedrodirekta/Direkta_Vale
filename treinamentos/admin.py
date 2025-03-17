from django.contrib import admin
from .models import Treinamento

@admin.register(Treinamento)
class TreinamentoAdmin(admin.ModelAdmin):
    list_display = ("funcionario", "nome_treinamento", "norma", "validade_passaporte", "get_status")

    def get_status(self, obj):
        return obj.calcular_status()[0]  # Retorna apenas o texto do status
    get_status.short_description = "Status"
