from ninja.errors import HttpError
from pedidos.models import Categoria


def get_categoria_by_id(categoria_id) -> Categoria | None:
    try:
        return Categoria.objects.get(pk=categoria_id)
    except Categoria.DoesNotExist:
        raise HttpError(404, f"Categoria de id {categoria_id} não encontrada.")
    
def categoria_save(nome: str) -> Categoria:
    categoria = Categoria.objects.create(nome=nome)

    return categoria

def categoria_update(categoria: Categoria, nome: str) -> Categoria:
    if nome != categoria.nome:
        categoria.nome = nome
        categoria.save()

    return categoria