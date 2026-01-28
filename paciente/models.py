from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import date


class Paciente(models.Model):

    SEXO_CHOICES=[
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paciente')
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
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return f"{self.nome_completo} - {self.cpf}"

    @property
    def email(self):
        return self.user.email
    
    @property
    def idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )