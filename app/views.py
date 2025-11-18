from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from .models import Sala, Reserva

# ----------------------------------------------------------------------
# Vista Principal (Listado de Salas)
# ----------------------------------------------------------------------
def inicio(request):
    """
    Renderiza la lista de salas disponibles y la interfaz de reserva, 
    con un enlace a la página de detalles para ver el estado completo.
    """
    # Filtra solo las salas habilitadas
    salas = Sala.objects.filter(activa=True).all()
    
    # Se añade un atributo 'estado' a cada sala para la visualización rápida
    for sala in salas:
        # La propiedad del modelo esta_disponible es usada para el estado rápido
        if sala.esta_disponible:
            sala.estado = "Disponible"
            sala.clase_estado = "bg-green-500"
        else:
            sala.estado = "Reservada"
            sala.clase_estado = "bg-red-500"

    contexto = {
        'titulo': 'Gestión de Salas de Estudio (ITID)',
        'mensaje': 'Consulta la disponibilidad de las salas. Presiona el nombre de la sala para ver detalles y reservar.',
        'salas': salas,
        'ahora': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
    }
    return render(request, 'app/index.html', contexto)

# ----------------------------------------------------------------------
# Lógica de Reserva (solo acepta POST)
# ----------------------------------------------------------------------
@require_POST
def reservar_sala(request, sala_id):
    """
    Maneja la lógica para crear una nueva reserva.
    """
    sala = get_object_or_404(Sala, pk=sala_id)
    rut = request.POST.get('rut_persona', '').strip()
    
    # 1. Validación de RUT (simulación básica)
    if not rut or len(rut) < 5:
        # Redirige a la página de detalles con error
        return redirect(f"{reverse('app:sala_detalle', args=[sala_id])}?error=RUT+inválido")

    # 2. Validación de Disponibilidad (Doble chequeo)
    if not sala.esta_disponible:
        return redirect(f"{reverse('app:sala_detalle', args=[sala_id])}?error=Sala+ya+reservada")

    # 3. Creación de la Reserva
    try:
        hora_inicio = timezone.now()
        duracion_maxima = timedelta(hours=2)
        hora_termino = hora_inicio + duracion_maxima
        
        Reserva.objects.create(
            sala=sala,
            rut_persona=rut,
            hora_inicio=hora_inicio,
            hora_termino=hora_termino
        )
        
        # Redirige a la página de detalles con mensaje de éxito
        termino_local = timezone.localtime(hora_termino).strftime('%H:%M')
        return redirect(f"{reverse('app:sala_detalle', args=[sala_id])}?exito=Reserva+exitosa.+Fin+de+la+reserva+a+las+{termino_local}.")

    except Exception as e:
        print(f"Error al intentar crear la reserva: {e}")
        return redirect(f"{reverse('app:sala_detalle', args=[sala_id])}?error=Error+interno+al+reservar")

# ----------------------------------------------------------------------
# Vista de Detalles de Sala (Nueva)
# ----------------------------------------------------------------------
def sala_detalle(request, sala_id):
    """
    Muestra los detalles de una sala específica, su estado actual y las reservas futuras.
    """
    # Filtramos por activa=True para que si se deshabilita/elimina, dé un 404
    sala = get_object_or_404(Sala, pk=sala_id, activa=True) 
    ahora = timezone.now()
    
    # Busca la reserva activa (si existe)
    reserva_actual = sala.reservas.filter(hora_termino__gt=ahora).order_by('hora_termino').first()
    
    # Busca las reservas futuras (excluyendo la actual si existe)
    reservas_futuras = sala.reservas.filter(hora_inicio__gt=ahora).order_by('hora_inicio')
    
    # Si hay una reserva_actual que también inicia en el futuro (poco probable pero posible),
    # la excluimos de la lista de reservas futuras si ya se manejó como 'reserva_actual'.
    if reserva_actual and reserva_actual in reservas_futuras:
        reservas_futuras = reservas_futuras.exclude(pk=reserva_actual.pk)

    contexto = {
        'titulo': f'Detalle de Sala: {sala.nombre}',
        'sala': sala,
        'reserva_actual': reserva_actual,
        'reservas_futuras': reservas_futuras[:5], # Mostrar las próximas 5 reservas
        'esta_disponible': sala.esta_disponible,
    }
    return render(request, 'app/sala_detalle.html', contexto)


# ----------------------------------------------------------------------
# Vista de Contacto (Mantenemos la vista original)
# ----------------------------------------------------------------------
def contacto(request):
    """
    Renderiza la plantilla de contacto.
    """
    contexto = {
        'titulo': 'Contáctanos',
        'mensaje': 'Por favor, usa esta página para enviar tus consultas.'
    }
    return render(request, 'app/index.html', contexto)