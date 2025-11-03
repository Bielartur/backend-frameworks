from ninja import Schema
from ninja.orm import ModelSchema
from typing import Optional

from ..models import Produto


class CategoriaOut(Schema):
    id: int
    nome: str


class ProdutoOut(ModelSchema):
    imagem: Optional[str] = None
    categoria: Optional[CategoriaOut] = None

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco', 'descricao', 'imagem', 'categoria', 'ativo']

