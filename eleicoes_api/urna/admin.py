from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Eleitor)
admin.site.register(Eleicao)
admin.site.register(Candidato)
admin.site.register(AptidaoEleitor)
admin.site.register(RegistroVotacao)
admin.site.register(Voto)

# nome e senha do admin: 
# nome: admin
# senha: 12345