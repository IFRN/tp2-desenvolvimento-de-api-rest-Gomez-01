from rest_framework import viewsets, filters
from .serializers import *
from .models import *


# Create your views here.

class EleitorViewSet(viewsets.ModelViewSet):
    queryset = Eleitor.objects.all()
    serializer_class = EleitorSerializer

    filter_backends = [filters.SearchFilter, filters.BaseFilterBackend]
    search_fields = ['nome', 'cpf', 'email']
    filterset_fields = ['ativo']
    
class EleicaoViewSet(viewsets.ModelViewSet):
    queryset = Eleicao.objects.all()
    serializer_class = EleicaoSerializer

    filter_backends = [filters.BaseFilterBackend, filters.OrderingFilter]
    
    filterset_fields = ['status', 'tipo', 'criada_por']
    search_fields = ['titulo']
    ordering_fields = ['data_inicio']
    ordering = ['-data_inicio']
    
class CandidatoViewSet(viewsets.ModelViewSet):
    queryset = Candidato.objects.all().select_related('eleicao')
    serializer_class = CandidatoSerializer

    filter_backends = [filters.SearchFilter, filters.BaseFilterBackend]
    
    filterset_fields = ['nome','nome_urna', 'partido_ou_chapa']

class AptidaoEleitorViewSet(viewsets.ModelViewSet):
    queryset = AptidaoEleitor.objects.all().select_related('eleitor', 'eleicao')
    serializer_class = AptidaoEleitorSerializer
    
    filter_backends = [filters.SearchFilter, filters.BaseFilterBackend]
    filterset_fields = ['eleitor', 'eleicao']
    
class RegistroVotacaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegistroVotacao.objects.all().select_related('eleitor', 'eleicao')
    serializer_class = RegistroVotacaoSerializer
    
    filter_backends = [filters.SearchFilter, filters.BaseFilterBackend, filters.OrderingFilter]
    filterset_fields = ['eleicao']
    ordering_fields = ['data_hora']
    ordering = ['-data_hora']
    
class VotoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Voto.objects.all()
    serializer_class = VotoSerializer
    
    filter_backends = [filters.SearchFilter, filters.BaseFilterBackend]
    filterset_fields = ['eleicao']
    