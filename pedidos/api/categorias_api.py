from ninja import Router
from typing import List, Optional

from core.api import ErrorSchema
from ..models import Categoria
from ..schemas.categorias_schemas import CategoriaOut, CategoriaIn
from pedidos.services import categorias_services as services

router = Router()


@router.post("/", response=CategoriaOut)
def criar_categoria(
    request,
    payload: CategoriaIn,
):
    categoria = services.categoria_save(payload.nome)

    return categoria


@router.get("/", response=List[CategoriaOut])
def listar_categorias(request):
    categorias = Categoria.objects.all()

    return categorias


@router.get("/{categoria_id}", response=CategoriaOut)
def obter_categoria(request, categoria_id: int):
    categoria = services.get_categoria_by_id(categoria_id)

    return categoria


@router.put("/{categoria_id}", response=CategoriaOut)
def atualizar_categoria(
    request,
    categoria_id: int,
    payload: CategoriaIn
):
    categoria = services.get_categoria_by_id(categoria_id)
    categoria_atualizada = services.categoria_update(categoria, payload.nome)

    return categoria_atualizada


@router.delete("/{categoria_id}", response={204: None, 404: ErrorSchema})
def deletar_categoria(request, categoria_id: int):
    categoria = services.get_categoria_by_id(categoria_id)
    categoria.delete()

    return 204, None
