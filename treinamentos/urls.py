from django.urls import path
from .views import lista_treinamentos

urlpatterns = [
    path("", lista_treinamentos, name="lista_treinamentos"),
]