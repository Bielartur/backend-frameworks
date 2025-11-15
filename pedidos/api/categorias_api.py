from ninja import Router
from typing import List, Optional

from ..models import Categoria
from ..schemas.categorias_schemas import (
    CategoriaResponse,
    CategoriaIn,
    CategoriasResponse,
)
from pedidos.services import categorias_services as services
from core.schemas import BaseResponse, ErrorSchema

router = Router(tags=["Categorias"])


@router.post("/", response=CategoriaResponse)
def criar_categoria(
    request,
    payload: CategoriaIn,
):
    categoria = services.categoria_save(payload.nome)

    return {"message": "Categoria salva com sucesso!", "data": categoria}


@router.get("/", response=CategoriasResponse)
def listar_categorias(request):
    categorias = Categoria.objects.all()

    return {"message": "Categorias encontradas com sucesso!", "data": categorias}


@router.get("/{categoria_id}", response=CategoriaResponse)
def obter_categoria(request, categoria_id: int):
    categoria = services.get_categoria_by_id(categoria_id)

    return {"message": "Categoria encontrada com sucesso!", "data": categoria}


@router.put("/{categoria_id}", response=CategoriaResponse)
def atualizar_categoria(request, categoria_id: int, payload: CategoriaIn):
    categoria = services.get_categoria_by_id(categoria_id)
    categoria_atualizada = services.categoria_update(categoria, payload.nome)

    return {"message": "Categoria encontrada com sucesso!", "data": categoria_atualizada}


@router.delete("/{categoria_id}", response={200: BaseResponse, 404: ErrorSchema})
def deletar_categoria(request, categoria_id: int):
    categoria = services.get_categoria_by_id(categoria_id)
    categoria.delete()

    return {
        "message": f"Categoria '{categoria.nome}' excluida com sucesso!",
        "data": None,
    }
