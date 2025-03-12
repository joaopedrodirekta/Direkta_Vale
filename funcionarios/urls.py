from django.urls import path
from . import views

urlpatterns = [
    path("cadastrar/", views.cadastrar_funcionario, name="cadastrar_funcionario"),
    path("listar/", views.listar_funcionarios, name="listar_funcionarios"),
]