from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@email.com", "senha123")
        return HttpResponse("Superusuário criado com sucesso!")
    return HttpResponse("Superusuário já existe!")

urlpatterns = [
    path("create-admin/", create_admin),  # Criando superusuário
    path("admin/", admin.site.urls),  # Ativando Django Admin
]