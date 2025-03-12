from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse

# Página inicial para evitar erro 404
def home(request):
    return render(request, "home.html")

# Página de usuário (apenas para testar)
def user_page(request):
    return HttpResponse("Página do Usuário - Em desenvolvimento")

urlpatterns = [
    path("", home, name="home"),  # Página inicial para evitar erro 404
    path("admin/", admin.site.urls),  # Django Admin
    path("usuario/", user_page),  # Página de usuário (ajuste conforme necessário)
    path("funcionarios/", include("funcionarios.urls")),  # App Funcionários
    path("treinamentos/", include("treinamentos.urls")),  # App Treinamentos
    path("inventario/", include("inventario.urls")),  # App Inventário
]