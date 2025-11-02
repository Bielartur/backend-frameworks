from django.db import models

from contas.models import Usuario

class Categoria(models.Model):
    nome = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.nome


# Create your models here.
class Cardapio(models.Model):
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
    item = models.ForeignKey(Cardapio, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    observacao = models.CharField(max_length=100, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.email}"