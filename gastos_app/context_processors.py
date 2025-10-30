from .models import Alerta

def alertas_context(request):
    """Incluye el número de alertas no leídas en todos los templates"""
    if request.user.is_authenticated:
        alertas_count = Alerta.objects.filter(usuario=request.user, leida=False).count()
        return {'alertas_count': alertas_count}
    return {'alertas_count': 0}