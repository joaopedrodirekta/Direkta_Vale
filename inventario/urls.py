from django.urls import path
from .views import lista_itens

urlpatterns = [
    path("", lista_itens, name="lista_itens"),
]