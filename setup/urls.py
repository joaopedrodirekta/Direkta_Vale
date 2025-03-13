from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve  # Adiciona suporte manual para mídia

# Página inicial para evitar erro 404
def home(request):
    return render(request, "home.html")

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("funcionarios/", include("funcionarios.urls")),
    path("treinamentos/", include("treinamentos.urls")),
    path("inventario/", include("inventario.urls")),
]

# Configuração para servir arquivos de mídia em produção no Render
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
    ]