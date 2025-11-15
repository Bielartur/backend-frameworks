from ninja.errors import HttpError
from ninja.files import UploadedFile
from pedidos.models import Produto
from core.utils.urls_utils import get_absolute_media_url
from ..schemas.produtos_schemas import ProdutoOut
from .categorias_services import get_categoria_by_id

from decimal import Decimal
from typing import Optional


def get_produto_by_id(produto_id) -> Produto | None:
    try:
        return Produto.objects.get(pk=produto_id)
    except Produto.DoesNotExist:
        raise HttpError(404, f"Produto de ID {produto_id} não encontrado")



def produto_save(
    nome: str, preco: Decimal, descricao: Optional[str], categoria_id: int, imagem: Optional[UploadedFile]
) -> Produto:
    categoria = get_categoria_by_id(categoria_id)

    produto = Produto.objects.create(
        nome=nome,
        preco=preco,
        descricao=descricao,
        categoria=categoria
    )

    if imagem:
        produto.imagem.save(imagem.name, imagem)

    produto.save()
    produto.refresh_from_db()

    return produto


def produto_update(
    produto: Produto,
    nome: Optional[str] = None,
    preco: Optional[Decimal] = None,
    descricao: Optional[str] = None,
    categoria_id: Optional[int] = None,
    imagem: Optional[UploadedFile] = None,
) -> Produto:
    produto.nome = nome if nome else produto.nome
    produto.preco = preco if preco else produto.preco
    produto.descricao = descricao if descricao else produto.descricao

    if categoria_id:
        categoria = get_categoria_by_id(categoria_id)    
        produto.categoria = categoria

    if imagem:
        produto.imagem.save(imagem.name, imagem)

    produto.save()
    produto.refresh_from_db()

    return produto
