from ninja import Schema
from ninja.orm import ModelSchema
from typing import Optional, List

from core.utils.urls_utils import get_absolute_media_url
from ..schemas.categorias_schemas import CategoriaOut
from ..models import Produto


class ProdutoOut(ModelSchema):
    imagem: Optional[str] = None
    categoria: Optional[CategoriaOut] = None

    class Meta:
        model = Produto
        fields = ["id", "nome", "preco", "descricao", "imagem", "categoria", "ativo"]

    @staticmethod
    def resolve_imagem(produto, context):
        request = context["request"]

        if produto.imagem:
            return get_absolute_media_url(request, produto.imagem.url)
        return None


class ProdutoResponse(Schema):
    message: str
    data: ProdutoOut


class ProdutosResponse(Schema):
    message: str
    data: List[ProdutoOut]
