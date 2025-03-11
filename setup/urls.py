from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from django.http import HttpResponse

# Página inicial para evitar erro 404
def home(request):
    return HttpResponse("Bem-vindo ao Django no Render! 🚀")

# Rota para criar o superusuário (remova depois de testar)
def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@email.com", "senha123")
        return HttpResponse("Superusuário criado com sucesso!")
    return HttpResponse("Superusuário já existe!")

# Página de usuário (apenas para testar)
def user_page(request):
    return HttpResponse("Página do Usuário - Em desenvolvimento")

urlpatterns = [
    path("", home),  # Página inicial para evitar erro 404
    path("admin/", admin.site.urls),  # Django Admin
    path("usuario/", user_page),  # Página de usuário (ajuste conforme necessário)
]