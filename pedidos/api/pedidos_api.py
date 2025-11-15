from ninja import Router
from ninja.errors import HttpError

from core.schemas import BaseResponse, ErrorSchema
from pedidos.schemas.pedidos_schemas import (
    PedidoIn,
    PedidoResponse,
    PedidoUpdate,
    PedidosResponse,
)
from pedidos.services import pedidos_services as services
from contas.services import auth_services

router = Router(tags=["Pedidos"])


@router.post("/", response=PedidoResponse)
def criar_pedido(request, payload: PedidoIn):
    usuario = auth_services.get_usuario_atual(request)

    try:
        pedido = services.pedido_save(usuario, payload)
    except ValueError as e:
        raise HttpError(400, str(e))

    return {"message": "Pedido criado com sucesso!", "data": pedido}


@router.get("/", response=PedidosResponse)
def listar_pedidos(request):
    pedidos = services.listar_pedidos()
    return {"message": "Pedidos encontrados com sucesso!", "data": pedidos}


@router.get("/{pedido_id}", response={200: PedidoResponse, 404: ErrorSchema})
def obter_pedido(request, pedido_id: int):
    pedido = services.get_pedido_by_id(pedido_id)
    return {"message": "Pedido encontrado com sucesso!", "data": pedido}


@router.put("/{pedido_id}", response={200: PedidoResponse, 404: ErrorSchema})
def atualizar_pedido(request, pedido_id: int, payload: PedidoUpdate):
    pedido = services.get_pedido_by_id(pedido_id)

    pedido.observacao = (
        payload.observacao if payload.observacao is not None else pedido.observacao
    )
    pedido.status = payload.status if payload.status is not None else pedido.status
    pedido.encerrado_em = (
        payload.encerrado_em
        if payload.encerrado_em is not None
        else pedido.encerrado_em
    )

    pedido.save(update_fields=["observacao", "status", "encerrado_em"])

    return {"message": "Pedido atualizado com sucesso!", "data": pedido}


@router.delete("/{pedido_id}", response={200: BaseResponse, 404: ErrorSchema})
def deletar_pedido(request, pedido_id: int):
    pedido = services.get_pedido_by_id(pedido_id)
    pedido.delete()

    return {"message": f"Pedido '{str(pedido)}' excluído com sucesso!", "data": pedido}
