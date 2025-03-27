from django.db import models

class ItemInventario(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    quantidade = models.PositiveIntegerField(default=0)
    local_armazenado = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.quantidade})"