from ninja import Router
from ninja.errors import HttpError
from typing import List

from pedidos.schemas.pedidos_schemas import PedidoIn, PedidoOut, PedidoUpdate
from pedidos.services import pedidos_services as services
from contas.services import auth_services

router = Router(tags=["Pedidos"])


@router.post('/', response=PedidoOut)
def criar_pedido(request, payload: PedidoIn):
    usuario = auth_services.get_usuario_atual(request)

    try:
        pedido = services.pedido_save(usuario, payload)
    except ValueError as e:
        raise HttpError(400, str(e))

    return pedido


@router.get('/', response=List[PedidoOut])
def listar_pedidos(request):
    return services.listar_pedidos()


@router.get("/{pedido_id}", response=PedidoOut)
def obter_pedido(request, pedido_id: int):
    return services.get_pedido_by_id(pedido_id)


@router.put("/{pedido_id}", response=PedidoOut)
def atualizar_pedido(request, pedido_id: int, payload: PedidoUpdate):
    pedido = services.get_pedido_by_id(pedido_id)

    pedido.observacao = payload.observacao if payload.observacao is not None else pedido.observacao
    pedido.status = payload.status if payload.status is not None else pedido.status
    pedido.encerrado_em = payload.encerrado_em if payload.encerrado_em is not None else pedido.encerrado_em

    pedido.save(update_fields=["observacao", "status", "encerrado_em"])

    return pedido


@router.delete('/{pedido_id}', response={204: None})
def deletar_pedido(request, pedido_id: int):
    pedido = services.get_pedido_by_id(pedido_id)
    pedido.delete()

    return 204, None