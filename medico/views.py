from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import Medico

# Assumindo que você tenha estes modelos (ajuste conforme necessário)
# from .models import Medico, Consulta


def medicos(request, id_medico):
    medico = get_object_or_404(Medico, id=id_medico)


    context = {
        'id_medico': id_medico,

    }
    
    return render(request, 'medicos.html',  {'medico': medico})


@login_required
def listar_consultas_medico(request, id_medico):
    """
    View para listar todas as consultas do médico
    """
    # medico = get_object_or_404(Medico, id=id_medico)
    
    # consultas = Consulta.objects.filter(medico=medico).order_by('-data', '-hora')
    
    context = {
        'id_medico': id_medico,
        # 'consultas': consultas,
    }
    
    return render(request, 'medicos/consultas_list.html', context)


@login_required
def iniciar_consulta(request, id_medico):
    """
    View para iniciar uma consulta
    """
    # medico = get_object_or_404(Medico, id=id_medico)
    
    # Lógica para iniciar consulta
    # Por exemplo: listar consultas agendadas para hoje e permitir iniciar
    
    context = {
        'id_medico': id_medico,
    }
    
    return render(request, 'medicos/iniciar_consulta.html', context)


@login_required
def encerrar_consulta(request, id_medico):
    """
    View para encerrar uma consulta
    """
    # medico = get_object_or_404(Medico, id=id_medico)
    
    # Lógica para encerrar consulta
    # Por exemplo: listar consultas em andamento e permitir encerrar
    
    context = {
        'id_medico': id_medico,
    }
    
    return render(request, 'medicos/encerrar_consulta.html', context)