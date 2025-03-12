from django.urls import path
from . import views
from .views import cadastrar_funcionario

urlpatterns = [
    path("cadastro/", cadastrar_funcionario, name="cadastrar_funcionario"),
    path("listar/", views.listar_funcionarios, name="listar_funcionarios"),
    path('funcionarios/ficha/<str:id_funcionario>/', views.ficha_funcionario, name='ficha_funcionario'),
]