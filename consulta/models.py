from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

# Importação dos models de outros apps
from paciente.models import Paciente
from medico.models import Medico


class Consulta(models.Model):

    
    STATUS_CHOICES = [
        ('AGENDADA', 'Agendada'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA_PACIENTE', 'Cancelada pelo Paciente'),
        ('CANCELADA_MEDICO', 'Cancelada pelo Médico'),
    ]
    
    TIPO_CONSULTA_CHOICES = [
        ('CLINICO_GERAL', 'Clínico Geral'),
        ('PEDIATRIA', 'Pediatria'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='consulta')
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name='consulta')
    data_consulta = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField(null=True, blank=True)
    tipo_consulta = models.CharField(max_length=20, choices=TIPO_CONSULTA_CHOICES)
    sintomas = models.TextField(blank=True, help_text='Sintomas relatados pelo paciente')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AGENDADA')
    diagnostico = models.TextField(blank=True)
    observacoes = models.TextField(blank=True, help_text="Observações do médico")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    avaliacao = models.IntegerField(null=True, blank=True,
        choices=[(i, i) for i in range(1, 6)],
        help_text="Avaliação do paciente (1 a 5 estrelas)"
    )
    comentario_avaliacao = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-data_consulta', '-horario_inicio']
        unique_together = ['medico', 'data_consulta', 'horario_inicio']
    
    def __str__(self):
        return f"Consulta {self.id} - {self.paciente.nome_completo} com {self.medico.nome_completo} em {self.data_consulta}"
    
    @property
    def pode_cancelar(self):
        '''Verifica se a consulta pode ser cancelada (com prazo mínimo)'''
        if self.status in ['CONCLUIDA', 'CANCELADA_PACIENTE', 'CANCELADA_MEDICO']:
            return False
        
        data_hora_consulta = datetime.combine(self.data_consulta, self.horario_inicio)
        prazo_minimo = datetime.now() + timedelta(hours=24)  # 24h de antecedência
        
        return data_hora_consulta > prazo_minimo
    
    @property
    def pode_reagendar(self):
        '''Verifica se a consulta pode ser reagendada'''
        return self.status in ['AGENDADA', ] and self.pode_cancelar
    
    @property
    def esta_ativa(self):
        '''Verifica se a consulta está ativa'''
        return self.status in ['AGENDADA', 'EM_ANDAMENTO']
    
    @property
    def pode_avaliar(self):
        '''Verifica se o paciente pode avaliar a consulta'''
        return self.status == 'CONCLUIDA' and self.avaliacao is None
    
    def iniciar_consulta(self):
        '''Método para iniciar a consulta'''
        if self.status == 'AGENDADA':
            self.status = 'EM_ANDAMENTO'
            self.horario_inicio = timezone.now().time()
            self.save()
            return True
        return False
    
    def encerrar_consulta(self, diagnostico, observacoes=''):
        '''Método para encerrar a consulta'''
        if self.status == 'EM_ANDAMENTO':
            self.status = 'CONCLUIDA'
            self.horario_fim = timezone.now().time()
            self.diagnostico = diagnostico
            if observacoes:
                self.observacoes = observacoes
            self.save()
            return True
        return False
    
    def cancelar_por_paciente(self):
        '''Método para cancelar consulta pelo paciente'''
        if self.pode_cancelar:
            self.status = 'CANCELADA_PACIENTE'
            self.save()
            return True
        return False
    
    def cancelar_por_medico(self):
        '''Método para cancelar consulta pelo médico'''
        if self.esta_ativa:
            self.status = 'CANCELADA_MEDICO'
            self.save()
            return True
        return False
