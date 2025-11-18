from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Ruta de administración
    path('admin/', admin.site.urls),
    
    # ------------------------------------
    # Conectamos las URLs de nuestra aplicación 'app'
    # La ruta principal (vacía) dirigirá a la aplicación 'app'
    path('', include('app.urls')),
    # ------------------------------------
]