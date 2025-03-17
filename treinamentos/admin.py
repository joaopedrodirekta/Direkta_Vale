from django.contrib import admin
from .models import Treinamento

@admin.register(Treinamento)
class TreinamentoAdmin(admin.ModelAdmin):
    list_display = ("funcionario", "nome_treinamento", "norma", "validade_passaporte", "get_status")
    list_filter = ("norma", "validade_passaporte")  
    search_fields = ("funcionario__nome_completo", "nome_treinamento")  
    ordering = ("validade_passaporte",)  

    def get_status(self, obj):
        if obj.validade_passaporte is None:
            return "Sem Validade"
        return obj.calcular_status()[0]  # Retorna apenas o texto do status

    get_status.short_description = "Status"