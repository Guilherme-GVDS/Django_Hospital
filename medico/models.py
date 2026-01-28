from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone


class Medico(models.Model):
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    ESPECIALIDADE_CHOICES = [
        ('CLINICO_GERAL', 'Clínico Geral'),
        ('PEDIATRIA', 'Pediatria'),
    ]
    
    STATUS_CHOICES = [
        ('ATIVO', 'Em Atividade'),
        ('FERIAS', 'Férias'),
        ('DESLIGADO', 'Desligado'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medico')
    nome_completo = models.CharField(max_length=200)
    foto= models.ImageField(upload_to='foto_perfil', blank=True, null=True,
                            default='static/imagens/default-perfil.jpg')
    cpf = models.CharField(max_length=11, unique=True,
        validators=[RegexValidator(r'^\d{11}$', 'CPF deve conter 11 dígitos')]
    )
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    celular = models.CharField(max_length=11,
        validators=[RegexValidator(r'^\d{10,11}$', 'Celular deve conter 10 ou 11 dígitos')]
    )
    cep = models.CharField(max_length=8,
        validators=[RegexValidator(r'^\d{8}$', 'CEP deve conter 8 dígitos')]
    )
    numero = models.CharField(max_length=10)
    data_admissao = models.DateField(default=timezone.now)
    especialidade = models.CharField(max_length=20, choices=ESPECIALIDADE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATIVO')
    
    class Meta:
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'
        ordering = ['nome_completo']
    
    def __str__(self):
        return f"Dr(a). {self.nome_completo} - {self.get_especialidade_display()}"
    
    @property
    def email(self):
        return self.user.email
    
    @property
    def esta_ativo(self):
        return self.status == 'ATIVO'