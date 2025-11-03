from ninja import Router, Form, File
from ninja.files import UploadedFile
from typing import List, Optional
from decimal import Decimal

from core.api import ErrorSchema
from ..models import Produto
from ..schemas.produtos_schemas import ProdutoOut
from pedidos.services import produtos_services as services

router = Router()


@router.post("/", response=ProdutoOut)
def criar_produto(
    request,
    nome: str = Form(...),
    preco: Decimal = Form(...),
    descricao: Optional[str] = Form(None),
    categoria_id: int = Form(...),
    imagem: Optional[UploadedFile] = File(None),
):
    produto = services.produto_save(nome, preco, descricao, categoria_id, imagem)
    payload = services.criar_produto_response(request, produto)

    return payload


@router.get("/", response=List[ProdutoOut])
def listar_produtos(request):
    produtos = Produto.objects.all()

    return [
        services.criar_produto_response(request, p)
        for p in produtos
    ]


@router.get("/{produto_id}", response=ProdutoOut)
def obter_produto(request, produto_id: int):
    produto = services.get_produto_by_id(produto_id)
    payload = services.criar_produto_response(request, produto)

    return payload


@router.put("/{produto_id}", response=ProdutoOut)
def atualizar_produto(
    request,
    produto_id: int,
    nome: Optional[str] = Form(None),
    preco: Optional[Decimal] = Form(None),
    descricao: Optional[str] = Form(None),
    categoria_id: Optional[int] = Form(None),
    imagem: Optional[UploadedFile] = File(None),
):
    produto = services.get_produto_by_id(produto_id)
    produto_atualizado = services.produto_update(produto, nome, preco, descricao, categoria_id, imagem)
    payload = services.criar_produto_response(request, produto_atualizado)

    return payload


@router.delete('/{produto_id}', response={204: None, 404: ErrorSchema})
def deletar_produto(request, produto_id: int):
    produto = services.get_produto_by_id(produto_id)
    produto.delete()

    return 204, None
