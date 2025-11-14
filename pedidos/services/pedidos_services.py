from django.db import transaction
from ninja.errors import HttpError
from typing import Iterable, Dict

from pedidos.schemas.pedidos_schemas import PedidoIn, ItemPedidoIn
from pedidos.models import ItensPedido, Pedido, Produto, Status


def get_pedido_by_id(pedido_id) -> Pedido | None:
    try:
        return Pedido.objects.get(pk=pedido_id)
    except Pedido.DoesNotExist:
        raise HttpError(404, f"Pedido de ID {pedido_id} não encontrado")


def listar_pedidos():
    return Pedido.objects.all()


def _salvar_itens_pedido(
        pedido: Pedido,
        produtos_dict: Dict[int, Produto],
        itens: Iterable[ItemPedidoIn],
) -> None:
    rows = []
    for i in itens:
        produto_id = i.produto_id
        quantidade = i.quantidade

        produto = produtos_dict.get(produto_id)
        if not produto:
            raise ValueError(f"Produto de ID {produto_id} não existe")

        preco = produto.preco

        rows.append(
            ItensPedido(
                pedido=pedido,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=preco,
            )
        )

    ItensPedido.objects.bulk_create(rows)


def pedido_save(usuario, payload: PedidoIn) -> Pedido:
    with transaction.atomic():
        pedido = Pedido.objects.create(
            usuario=usuario,
            observacao=(payload.observacao or "")
        )

        ids = [i.produto_id for i in payload.itens]
        # o in_bulk pega todos os produtos que estejam dentro dessa lista de IDs
        produtos_dict = Produto.objects.in_bulk(ids)

        _salvar_itens_pedido(pedido, produtos_dict, payload.itens)

        pedido.atualizar_total()
        pedido.refresh_from_db()

    return pedido
