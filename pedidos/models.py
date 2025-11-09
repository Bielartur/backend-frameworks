from django.db import models
from django.db.models import Sum, F, DecimalField

from contas.models import Usuario

class Categoria(models.Model):
    nome = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.nome


# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='cardapio/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"


class Status(models.TextChoices):
    PENDENTE = 'pendente', 'Pendente'
    CONCLUIDO = 'concluido', 'Concluído'  # Não pode acento
    CANCELADO = 'cancelado', 'Cancelado'


class Pedido(models.Model):
    itens = models.ManyToManyField('Produto', through='ItensPedido', related_name='pedidos')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    observacao = models.CharField(max_length=100, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    encerrado_em = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)

    def atualizar_total(self):
        soma = (
            self.itens_pedido
            .aggregate(
                total=Sum(F('quantidade') * F('preco_unitario'), output_field=DecimalField())
            )['total'] or 0
        )
        self.total = soma
        self.save(update_fields=['total'])
        return soma

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.email}"
    

class ItensPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens_pedido')
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING, related_name='itens_pedido')
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario
