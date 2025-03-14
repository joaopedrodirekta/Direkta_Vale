from django.urls import path
from . import views
from .views import cadastrar_treinamento

urlpatterns = [
    path('cadastrar/', cadastrar_treinamento, name='cadastrar_treinamento'),
    path("dashboard/", views.dashboard_treinamentos, name="dashboard_treinamentos"),
]