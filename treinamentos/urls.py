from django.urls import path
from . import views

urlpatterns = [
    path("cadastrar/", views.cadastrar_treinamento, name="cadastrar_treinamento"),
    path("dashboard/", views.dashboard_treinamentos, name="dashboard_treinamentos"),
]