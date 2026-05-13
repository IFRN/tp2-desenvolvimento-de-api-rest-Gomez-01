from rest_framework import serializers
from .models import *
from django.utils import timezone
import re

class EleitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleitor
        fields = '__all__'

    def validate_cpf(self, value):
        """
        Valida se o CPF está no formato 000.000.000-00
        """
        # Regex para o formato exato solicitado
        cpf_regex = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
        
        if not re.match(cpf_regex, value):
            raise serializers.ValidationError(
                "O CPF deve estar no formato 000.000.000-00"
            )
        
        return value
        
class EleicaoSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display')
    total_aptos = serializers.IntegerField(source='aptos.count')
    total_candidatos = serializers.SerializerMethodField()
    
    class Meta:
        model = Eleicao
        fields = '__all__'
        
    def get_total_candidatos(self, obj):
        return obj.candidatos.count()
        
class CandidatoSerializer(serializers.ModelSerializer):
    eleicao_titulo = serializers.CharField(source='eleicao.titulo', read_only=True)
    
    class Meta:
        model = Candidato
        fields = '__all__'

class AptidaoEleitorSerializer(serializers.ModelSerializer):
    eleitor_nome = serializers.CharField(source='eleitor.nome', read_only=True)
    eleicao_titulo = serializers.CharField(source='eleicao.titulo', read_only=True)
    
    class Meta:
        model = AptidaoEleitor
        fields = '__all__'
        
class RegistroVotacaoSerializer(serializers.ModelSerializer):
    eleitor_nome = serializers.CharField(source='eleitor.nome', read_only=True)
    eleicao_titulo = serializers.CharField(source='eleicao.titulo', read_only=True)
    
    class Meta:
        model = RegistroVotacao
        fields = ['eleitor', 'eleicao', 'data_hora', 'eleitor_nome', 'eleicao_titulo']
        read_only_fields = ['eleitor', 'eleicao', 'data_hora', 'eleitor_nome', 'eleicao_titulo' ]

class VotoSerializer(serializers.ModelSerializer):
    candidato_nome_urna = serializers.CharField(source='candidato.nome_urna',read_only=True, allow_null=True)
    em_branco_display = serializers.SerializerMethodField()

    class Meta:
        model = Voto
        fields = ['id','eleicao','candidato','candidato_nome_urna','em_branco','em_branco_display', 'data_hora']
        read_only_fields = ['id', 'eleicao', 'candidato', 'em_branco', 'data_hora']

    def get_em_branco_display(self, obj):
        return 'BRANCO' if obj.em_branco else None
    
class VotacaoInputSerializer(serializers.Serializer):
    eleitor_id = serializers.IntegerField()
    eleicao_id = serializers.IntegerField()
    candidato_id = serializers.IntegerField(required=False, allow_null=True)
    em_branco = serializers.BooleanField(default=False)

    def validate(self, data):

        try:
            eleicao = Eleicao.objects.get(pk=data['eleicao_id'])
        except Eleicao.DoesNotExist:
            raise serializers.ValidationError({"eleicao_id": "Eleição não encontrada."})
        try:
            eleitor = Eleitor.objects.get(pk=data['eleitor_id'])
        except Eleitor.DoesNotExist:
            raise serializers.ValidationError({"eleitor_id": "Eleitor não encontrado."})

        if eleicao.status != 'aberta': #(a)
            raise serializers.ValidationError("Esta eleição não está aberta para votação.")
        
        agora = timezone.now()
        if not (eleicao.data_inicio <= agora <= eleicao.data_fim): #(b)
            raise serializers.ValidationError("A eleição não está no período de votação vigente.")

        if not eleitor.esta_apto(eleicao): #(c)
            raise serializers.ValidationError("eleitor inapto.")

        if RegistroVotacao.objects.filter(eleitor=eleitor, eleicao=eleicao).exists(): #(d)
            raise serializers.ValidationError("Este eleitor votou nesta eleição.")
        
        candidato_id = data.get('candidato_id') #(f)  
        em_branco = data.get('em_branco') 
        if em_branco and candidato_id:
            raise serializers.ValidationError("Não pode votar em um candidato e em branco.")
        if not em_branco and not candidato_id:
            raise serializers.ValidationError("Você deve escolher um candidato ou votar em branco.")

        if candidato_id: #(e)
            try:
                candidato = Candidato.objects.get(pk=candidato_id)
                if candidato.eleicao != eleicao:
                    raise serializers.ValidationError("O candidato informado não pertence a esta eleição.")
            except Candidato.DoesNotExist:
                raise serializers.ValidationError("Candidato não encontrado.")

        return data