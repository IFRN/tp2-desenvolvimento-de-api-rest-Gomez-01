from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Eleitor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
class Eleicao(models.Model):
    TIPO_CHOICES = (
        ('estudantil', 'Estudantil'),
        ('sindical', 'Sindical'),
        ('associacao', 'Associacao'),
        ('condominio', 'Condominio'),
        ('conselho', 'Conselho'),
        ('outra', 'Outra'),
    )
    STATUS_CHOICES = (
        ('rascunho', 'Rascunho'),
        ('aberta', 'Aberta'),
        ('encerrada', 'Encerrada'),
        ('apurada', 'Apurada'),
    )
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(choices=TIPO_CHOICES)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    status = models.CharField(max_length=20, default='rascunho')
    permite_branco = models.BooleanField(default=True)
    criada_por = models.ForeignKey(
        Eleitor,
        on_delete=models.PROTECT,
        related_name='eleicoes_criadas'
    )

    def __str__(self):
        return self.titulo
    
    def clean(self):
        if self.data_inicio >= self.data_fim:
            raise ValidationError('A data de início deve ser antes da data de fim.')
        
        if self.pk:
            eleicao_atual = Eleicao.objects.get(pk=self.pk)
            if self.status != eleicao_atual.status:
                fluxo = ['rascunho', 'aberta', 'encerrada', 'apurada']
                status_atual = fluxo.index(eleicao_atual.status)
                novo_status = fluxo.index(self.status)
                if novo_status != status_atual + 1:
                    raise ValidationError('O fluxo é: rascunho > aberta > encerrada > apurada e não pode voltar ou pular etapas.')
        
class Candidato(models.Model):
    eleicao = models.ForeignKey(
        Eleicao,
        on_delete=models.CASCADE,
        related_name='candidatos'
    )
    numero = models.PositiveIntegerField()
    nome = models.CharField(max_length=150)
    nome_urna = models.CharField(max_length=50)
    partido_ou_chapa = models.CharField(max_length=100, blank=True)
    proposta = models.TextField(blank=True)
    foto_url = models.URLField(blank=True)
    
    class Meta:
        unique_together = [('eleicao', 'numero')]
        
class AptidaoEleitor(models.Model):
    eleitor = models.ForeignKey(
        Eleitor,
        on_delete=models.PROTECT,
        related_name='aptidoes'
    )
    eleicao = models.ForeignKey(
        Eleicao, 
        on_delete=models.CASCADE,
        related_name='aptos'
    )
    data_inclusao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [('eleitor', 'eleicao')]
        
class RegistroVotacao(models.Model):
    eleitor = models.ForeignKey(
        Eleitor,
        on_delete=models.PROTECT,
        related_name='registros_votacao'
    )
    eleicao = models.ForeignKey(
        Eleicao,
        on_delete=models.PROTECT,
        related_name='registros_votacao'
    )
    data_hora = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [('eleitor', 'eleicao')]

    def __str__(self):
        return f'{self.eleitor.nome} votou em {self.eleicao.titulo} em {self.data_hora}'
        
    
class Voto(models.Model):
    eleicao = models.ForeignKey(
        Eleicao,
        on_delete=models.PROTECT,
        related_name='votos'
    )
    candidato = models.ForeignKey(
        Candidato,
        on_delete=models.PROTECT,
        related_name='votos',
        null=True,
        blank=True
    )
    voto_branco = models.BooleanField(default=False)
    em_branco = models.BooleanField(default=False)
    data_hora = models.DateTimeField(auto_now_add=True)
    comprovante_hash = models.CharField(max_length=64, unique=True)
    
    def clean(self):
        if self.em_branco and self.candidato is not None:
            raise ValidationError('Voto em branco não pode ter candidato.')
        if not self.em_branco and self.candidato is None:
            raise ValidationError('Voto em branco não pode ter candidato.')
        