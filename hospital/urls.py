"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import Homepage
#from paciente.views import pacientes
import paciente.views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Homepage.as_view()),
    #path('paciente/', include('paciente.urls')),
    path('paciente/<int:id>/', paciente.views.pacientes, name='pacientes'),
    path('paciente/<int:id_paciente>/agendar/', paciente.views.agendar_consulta, name='agendar_consulta'),
    path('paciente/<int:id_paciente>/consultas/', paciente.views.listar_consultas, name='consultas'),

    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)