from django.urls import path
from . import views

app_name = "treinamentos"  # Define um namespace para evitar conflitos de URL

urlpatterns = [
    path("cadastrar/", views.cadastrar_treinamento, name="cadastrar_treinamento"),
    path("dashboard/", views.dashboard_treinamentos, name="dashboard_treinamentos"),
]