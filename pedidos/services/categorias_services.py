from ninja.errors import HttpError
from pedidos.models import Categoria


def get_categoria_by_id(categoria_id) -> Categoria | None:
    try:
        return Categoria.objects.get(pk=categoria_id)
    except Categoria.DoesNotExist:
        raise HttpError(404, f"Categoria de id {categoria_id} não encontrada.")
