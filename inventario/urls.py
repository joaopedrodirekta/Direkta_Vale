from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventario_home, name='inventario_home'),
    path('cadastro/', views.cadastrar_item, name='cadastrar_item'),
    path('listar/', views.listar_inventario, name='listar_inventario'),
    path('imprimir/', views.imprimir_lista, name='imprimir_lista'),
]