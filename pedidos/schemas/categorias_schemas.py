from ninja import Schema
from typing import List


class CategoriaIn(Schema):
    nome: str


class CategoriaOut(Schema):
    id: int
    nome: str


class CategoriasResponse(Schema):
    message: str
    data: List[CategoriaOut]


class CategoriaResponse(Schema):
    message: str
    data: CategoriaOut
