from ninja import NinjaAPI, Schema
from ninja.errors import HttpError
from ninja.parser import Parser
from django.http import Http404
import orjson


class ErrorSchema(Schema):
    error: str


class ORJsonParser(Parser):
    def parser_body(self, request):
        return orjson.loads(request.body)

api = NinjaAPI(parser=ORJsonParser(), urls_namespace="api")


@api.exception_handler(Http404)
def not_found_handler(request, exc):
    message = exc.args[0] if exc.args else "Elemento não encontrado"

    return api.create_response(
        request,
        {"error": message},
        status=404
    )


@api.exception_handler(HttpError)
def http_error_handler(request, exc: HttpError):
    return api.create_response(
        request,
        {"error": str(exc)},  # sempre segue o ErrorSchema
        status=exc.status_code,
    )


api.add_router("/produtos/", "pedidos.api.produtos_api.router")
api.add_router("/categorias/", "pedidos.api.categorias_api.router")
# api.add_router("auth", "contas.api.router")
