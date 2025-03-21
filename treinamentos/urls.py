from django.urls import path
from . import views
from .views import exportar_excel, exportar_pdf, atualizar_treinamento, excluir_treinamento

urlpatterns = [
    path("cadastrar/", views.cadastrar_treinamento, name="cadastrar_treinamento"),
    path("dashboard/", views.dashboard_treinamentos, name="dashboard_treinamentos"),
    path("exportar-excel/", exportar_excel, name="exportar_excel"),
    path("exportar-pdf/", exportar_pdf, name="exportar_pdf"),
    path('atualizar/<int:treinamento_id>/', atualizar_treinamento, name='atualizar_treinamento'),
    path("excluir/<int:treinamento_id>/", excluir_treinamento, name="excluir_treinamento"),
]