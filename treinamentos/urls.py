from django.urls import path
from . import views
from .views import exportar_excel, exportar_pdf, atualizar_treinamento, excluir_treinamento, editar_treinamentos_funcionario, atualizar_treinamento_ajax

urlpatterns = [
    path("cadastrar/", views.cadastrar_treinamento, name="cadastrar_treinamento"),
    path("dashboard/", views.dashboard_treinamentos, name="dashboard_treinamentos"),
    path('listar/', views.listar_treinamentos, name='listar_treinamentos'),
    path("exportar-excel/", exportar_excel, name="exportar_excel"),
    path("exportar-pdf/", exportar_pdf, name="exportar_pdf"),
    path('atualizar/<int:treinamento_id>/', atualizar_treinamento, name='atualizar_treinamento'),
    path('treinamentos/excluir/<int:treinamento_id>/', views.excluir_treinamento, name='excluir_treinamento'),
    path('treinamentos/editar/<str:id_funcionario>/', editar_treinamentos_funcionario, name='editar_treinamentos_funcionario'),
    path("ajax/atualizar/", atualizar_treinamento_ajax, name="atualizar_treinamento_ajax"),
]