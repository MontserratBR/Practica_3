# app_gestion_taller/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # aquí van tus rutas, por ejemplo:
    path('', views.index, name='index'),
]