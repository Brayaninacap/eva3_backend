from django.db import models
from django.utils import timezone
from datetime import timedelta

class Sala(models.Model):
    """
    Modelo para gestionar las salas de estudio.
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Sala")
    capacidad_maxima = models.IntegerField(verbose_name="Capacidad Máxima")
    activa = models.BooleanField(default=True, verbose_name="Sala Habilitada")

    class Meta:
        verbose_name = "Sala de Estudio"
        verbose_name_plural = "Salas de Estudio"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
    # Propiedad calculada para determinar la disponibilidad en tiempo real
    @property
    def esta_disponible(self):
        """
        Verifica si la sala tiene alguna reserva activa en este momento.
        """
        ahora = timezone.now()
        # Busca reservas activas (hora_termino > ahora) para esta sala
        reserva_activa = self.reservas.filter(hora_termino__gt=ahora).exists()
        return not reserva_activa and self.activa

class Reserva(models.Model):
    """
    Modelo para gestionar las reservas de salas.
    """
    sala = models.ForeignKey(
        Sala, 
        on_delete=models.CASCADE, 
        related_name='reservas',
        verbose_name="Sala Reservada"
    )
    rut_persona = models.CharField(max_length=12, verbose_name="RUT del Estudiante")
    hora_inicio = models.DateTimeField(default=timezone.now, verbose_name="Hora de Inicio")
    # Hora de término, por defecto 2 horas después del inicio
    hora_termino = models.DateTimeField(verbose_name="Hora de Término")

    class Meta:
        verbose_name = "Reserva de Sala"
        verbose_name_plural = "Reservas de Salas"
        ordering = ['-hora_inicio']
    
    # Sobrescribimos el método save para asegurar que la hora_termino se establezca
    # con un máximo de 2 horas.
    def save(self, *args, **kwargs):
        # Si hora_termino no está definido (primera creación), se establece a +2h
        if not self.id:
            # Asegura que la duración máxima es 2 horas
            max_duracion = timedelta(hours=2)
            self.hora_termino = self.hora_inicio + max_duracion
        super().save(*args, **kwargs)

    def __str__(self):
        # Muestra Sala, RUT e Inicio
        return f"Reserva de {self.sala.nombre} por {self.rut_persona} ({self.hora_inicio.strftime('%H:%M')})"
