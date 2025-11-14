from ninja import Schema
from decimal import Decimal
from ninja.orm import ModelSchema
from typing import List, Annotated, Optional
from pydantic import Field, field_validator, computed_field
from datetime import datetime
from enum import Enum

from core.utils.urls_utils import get_absolute_media_url
from ..models import Pedido, Produto, ItensPedido

QuantidadePositiva = Annotated[int, Field(gt=0)]


class ProdutoOutResumido(ModelSchema):
    imagem: Optional[str] = None

    class Meta:
        model = Produto
        fields = ["id", "nome", "preco", "imagem"]

    @staticmethod
    def resolve_imagem(produto, context):
        request = context["request"]

        if produto.imagem:
            return get_absolute_media_url(request, produto.imagem.url)
        return None


class ItemPedidoOut(ModelSchema):
    produto: ProdutoOutResumido  # aninha o produto do item
    subtotal: Decimal

    class Meta:
        model = ItensPedido
        fields = ["id", "produto", "quantidade", "preco_unitario"]

    @staticmethod
    def resolve_subtotal(obj) -> Decimal:
        # usa a property do modelo
        return obj.subtotal


class ItemPedidoIn(Schema):
    produto_id: int
    quantidade: QuantidadePositiva


class PedidoIn(ModelSchema):
    itens: List[ItemPedidoIn]

    class Meta:
        model = Pedido
        fields = ["observacao"]


class PedidoOut(ModelSchema):
    itens: List[ItemPedidoOut]
    status_legivel: str  # label amigável do status

    class Meta:
        model = Pedido
        fields = ["id", "usuario", "observacao", "total", "status", "criado_em", "encerrado_em"]

    # --- Itens ---
    @staticmethod
    def resolve_itens(obj):
        return obj.itens_pedido.all()

    # --- Usuário ---
    @staticmethod
    def resolve_usuario(obj):
        return obj.usuario.email

    # --- Status legível ---
    @staticmethod
    def resolve_status_legivel(obj) -> str:
        """
        Retorna a label humana do campo 'status' (choices do modelo).
        """
        return obj.get_status_display()

    # --- Data formatada (criado_em) ---
    @computed_field
    @property
    def criado_em_formatado(self) -> str | None:
        if not self.criado_em:
            return None
        return self.criado_em.strftime("%d/%m/%Y %H:%M")

    # --- Data formatada (encerrado_em) ---
    @computed_field
    @property
    def encerrado_em_formatado(self) -> str | None:
        if not self.encerrado_em:
            return None
        return self.encerrado_em.strftime("%d/%m/%Y %H:%M")


class PedidoUpdate(ModelSchema):
    class Meta:
        model = Pedido
        fields = ["observacao", "status", "encerrado_em"]
        optional = ["observacao", "status", "encerrado_em"]

    @field_validator("encerrado_em", mode="before", check_fields=False)
    def parse_encerrado_em(cls, value):
        if not value:
            return None
        if isinstance(value, datetime):
            return value

        formatos = [
            "%Y-%m-%d %H:%M",
            "%d/%m/%Y %H:%M",
            "%d/%m/%Y",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%S",
        ]
        for fmt in formatos:
            try:
                return datetime.strptime(value, fmt)
            except (ValueError, TypeError):
                pass
        raise ValueError("Formato de data inválido. Use DD/MM/AAAA HH:MM.")
