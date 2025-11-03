from ninja.orm import ModelSchema
from typing import Optional

from ..schemas.categorias_schemas import CategoriaOut
from ..models import Produto


class ProdutoOut(ModelSchema):
    imagem: Optional[str] = None
    categoria: Optional[CategoriaOut] = None

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco', 'descricao', 'imagem', 'categoria', 'ativo']

