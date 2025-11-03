from ninja import Schema


class CategoriaIn(Schema):
    nome : str


class CategoriaOut(Schema):
    id: int
    nome: str
