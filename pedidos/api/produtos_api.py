from ninja import Router, Form, File
from ninja.files import UploadedFile
from typing import List, Optional
from decimal import Decimal

from core.schemas import BaseResponse, ErrorSchema
from ..models import Produto
from ..schemas.produtos_schemas import ProdutoResponse, ProdutosResponse
from pedidos.services import produtos_services as services

router = Router(tags=["Produtos"])


@router.post("/", response=ProdutoResponse)
def criar_produto(
    request,
    nome: str = Form(...),
    preco: Decimal = Form(...),
    descricao: Optional[str] = Form(None),
    categoria_id: int = Form(...),
    imagem: Optional[UploadedFile] = File(None),
):
    produto = services.produto_save(nome, preco, descricao, categoria_id, imagem)

    return {"message": "Produto criado com sucesso!", "data": produto}


@router.get("/", response=ProdutosResponse)
def listar_produtos(request):
    produtos = Produto.objects.all()

    return {"message": "Produtos encontrados com sucesso!", "data": produtos}


@router.get("/{produto_id}", response=ProdutoResponse)
def obter_produto(request, produto_id: int):
    produto = services.get_produto_by_id(produto_id)

    return {"message": "Produto criado com sucesso!", "data": produto}


@router.put("/{produto_id}", response=ProdutoResponse)
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
    produto_atualizado = services.produto_update(
        produto, nome, preco, descricao, categoria_id, imagem
    )

    return {"message": "Produto  atualizado com sucesso!", "data": produto_atualizado}


@router.delete("/{produto_id}", response={200: BaseResponse, 404: ErrorSchema})
def deletar_produto(request, produto_id: int):
    produto = services.get_produto_by_id(produto_id)
    produto.delete()

    return {"message": f"Produto '{str(produto)}' excluído com sucesso!", "data": None}
