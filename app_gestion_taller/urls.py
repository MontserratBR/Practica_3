# app_gestion_taller/urls.py
from operator import index

from django.urls import path
from .views import all_clientes, all_coches, all_servicios, buscar_cliente, filtrar_coche, registrar_cliente, registrar_coche, registrar_servicio, detalle_cliente
from . import views

urlpatterns = [
    # aquí van tus rutas, por ejemplo:
    path('', index, name='index'),
    path('clientes/registrar/', registrar_cliente, name='registrar_cliente'),
    path('coches/registrar/', registrar_coche, name='registrar_coche'),
    path('servicios/registrar/', registrar_servicio, name='registrar_servicio'),
    path('clientes/<str:cliente_nombre>/', buscar_cliente, name='buscar_cliente'),
    path('clientes/', all_clientes, name='all_clientes'),
    path('coches/', all_coches, name='all_coches'),
    path('servicios/', all_servicios, name='all_servicios'),
    path('coches/filtrar/<str:modelo>/', filtrar_coche, name='filtrar_coche'),
    path('clientes/<str:cliente_nombre>/servicios/', views.servicios_cliente, name='servicios_cliente'),
    path('clientes/detalle/<int:cliente_id>/', detalle_cliente, name='detalle_cliente'),

]
