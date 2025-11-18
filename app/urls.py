from django.urls import path
from . import views  # Importamos las vistas de la aplicación

# Definimos el nombre de la aplicación para el namespace
app_name = 'app'

urlpatterns = [
    # 1. Ruta de listado y visualización principal
    path('', views.inicio, name='inicio'),
    
    # 2. Ruta de detalles de sala (NUEVA)
    path('sala/<int:sala_id>/', views.sala_detalle, name='sala_detalle'),
    
    # 3. Ruta para procesar la reserva (POST)
    path('reservar/<int:sala_id>/', views.reservar_sala, name='reservar_sala'),
    
    # 4. Mantenemos la vista de contacto original
    path('contacto/', views.contacto, name='contacto'),
]