from django.contrib import admin
from .models import Sala, Reserva
from django.utils import timezone 

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    """
    Gestión de Salas de Estudio para el administrador. Permite agregar, editar,
    eliminar y cambiar el estado de activación (habilitar/deshabilitar).
    
    NOTA: Al eliminar una Sala, todas sus Reservas asociadas son eliminadas 
    automáticamente debido a la configuración models.CASCADE en el modelo Reserva.
    """
    # Campos mostrados en la lista
    list_display = ('nombre', 'capacidad_maxima', 'activa', 'mostrar_disponibilidad_admin')
    # Filtros laterales
    list_filter = ('activa', 'capacidad_maxima')
    # Campos de búsqueda
    search_fields = ('nombre',)
    
    # Propiedad para mostrar la disponibilidad en el Admin
    def mostrar_disponibilidad_admin(self, obj):
        # Devuelve el texto descriptivo
        return "Reservada" if not obj.esta_disponible else "Disponible"
    mostrar_disponibilidad_admin.short_description = "Disponibilidad Actual"
    # IMPORTANTE: Eliminamos 'mostrar_disponibilidad_admin.boolean = True'
    # para evitar el KeyError, ya que devuelve una cadena de texto, no un booleano.

    # Acción para "Habilitar Sala"
    @admin.action(description='Habilitar Salas seleccionadas')
    def habilitar_salas(self, request, queryset):
        queryset.update(activa=True)
        self.message_user(request, f"{queryset.count()} salas han sido habilitadas.")
        
    # Acción para "Deshabilitar Sala"
    @admin.action(description='Deshabilitar Salas seleccionadas')
    def deshabilitar_salas(self, request, queryset):
        queryset.update(activa=False)
        self.message_user(request, f"{queryset.count()} salas han sido deshabilitadas.")

    actions = [habilitar_salas, deshabilitar_salas]

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    """
    Gestión de Reservas.
    """
    # Campos mostrados en la lista
    list_display = ('sala', 'rut_persona', 'hora_inicio', 'hora_termino', 'es_activa')
    # Filtros laterales
    list_filter = ('sala', 'hora_inicio')
    # Campos de búsqueda
    search_fields = ('rut_persona', 'sala__nombre')
    # Campos de solo lectura (no permite al admin modificar las horas)
    readonly_fields = ('hora_inicio', 'hora_termino') 
    
    def es_activa(self, obj):
        # Verifica si la hora de término es posterior a la hora actual
        return obj.hora_termino > timezone.now()
    es_activa.short_description = "Reserva Activa"
    es_activa.boolean = True # Correcto, ya que devuelve un booleano

    # -------------------------------------------------------------
    # ACCIÓN ADMINISTRATIVA: Limpiar Reservas Terminadas
    # -------------------------------------------------------------
    @admin.action(description='Eliminar reservas cuya hora de término ya pasó')
    def limpiar_reservas_inactivas(self, request, queryset):
        """
        Elimina todas las reservas seleccionadas que ya han finalizado 
        (hora_termino anterior a la hora actual).
        """
        ahora = timezone.now()
        # Filtra el queryset para asegurar que solo se borran las que ya terminaron
        reservas_a_borrar = queryset.filter(hora_termino__lt=ahora)
        conteo = reservas_a_borrar.count()
        reservas_a_borrar.delete()
        self.message_user(request, f"{conteo} reservas terminadas han sido eliminadas.")

    actions = [limpiar_reservas_inactivas]