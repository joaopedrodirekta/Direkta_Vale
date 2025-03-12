from django.contrib import admin
from .models import Funcionario

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id_funcionario', 'nome_completo', 'cpf', 'departamento', 'status')
    search_fields = ('nome_completo', 'cpf')
    list_filter = ('status', 'departamento')