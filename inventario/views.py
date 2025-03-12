from django.shortcuts import render
from django.http import HttpResponse

def inventario_home(request):
    return render(request, "inventario/home.html")