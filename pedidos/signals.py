from django.db import transaction
from django.utils import timezone
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import ItensPedido, Pedido, Status


@receiver([post_save, post_delete], sender=ItensPedido)
def recalc_total_on_item_change(sender, instance, **kwargs):
    pedido = instance.pedido
    # evita recálculo antes do commit em transações
    transaction.on_commit(lambda: pedido.atualizar_total())


@receiver(pre_save, sender=Pedido)
def definir_data_encerramento(sender, instance: Pedido, **kwargs):
    """
    Define automaticamente a data de encerramento quando o pedido
    é alterado para 'CONCLUIDO' ou 'CANCELADO'.
    """
    if not instance.pk:
        # Novo pedido sendo criado -> ainda não existe no BD
        return

    try:
        # Obtém o estado anterior do pedido
        pedido_antigo = Pedido.objects.get(pk=instance.pk)
    except Pedido.DoesNotExist:
        return

    # Se o status foi alterado
    status_antigo = pedido_antigo.status
    status_novo = instance.status

    # E o novo status é concluído ou cancelado
    if status_antigo != status_novo and status_novo in [Status.CONCLUIDO, Status.CANCELADO]:
        instance.encerrado_em = timezone.now()

    elif status_novo == Status.PENDENTE:
        instance.encerrado_em = None
