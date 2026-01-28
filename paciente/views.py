from django.shortcuts import render, get_object_or_404
from.models import Paciente

# Create your views here.
def pacientes(request, id):
    paciente = get_object_or_404(Paciente, id=id) 

    consulta_ativa = False  # Placeholder - ajuste conforme seu modelo de Consulta
    
    context = {
        'paciente': paciente,
        'consulta_ativa': consulta_ativa,
    }

    return render(request, 'pacientes.html', {'paciente': paciente})

# @login_required
def agendar_consulta(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    # Lógica para agendar consulta
    return render(request, 'pacientes/agendar_consulta.html', {'paciente': paciente})

# @login_required
def listar_consultas(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    # Lógica para listar consultas
    consultas = paciente.consultas.all()  # Ajuste conforme seu modelo
    return render(request, 'pacientes/consultas.html', {
        'paciente': paciente,
        'consultas': consultas
    })

