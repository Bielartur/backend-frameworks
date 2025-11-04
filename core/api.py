from ninja import NinjaAPI
from ninja.errors import HttpError
from ninja.parser import Parser
from django.http import Http404
import orjson
from .auth import jwt_auth



class ORJsonParser(Parser):
    def parser_body(self, request):
        return orjson.loads(request.body)


api = NinjaAPI(parser=ORJsonParser(), urls_namespace="api")


@api.exception_handler(Http404)
def not_found_handler(request, exc):
    message = exc.args[0] if exc.args else "Elemento não encontrado"

    return api.create_response(request, {"error": message}, status=404)


@api.exception_handler(HttpError)
def http_error_handler(request, exc: HttpError):
    return api.create_response(
        request,
        {"error": str(exc)},  # sempre segue o ErrorSchema
        status=exc.status_code,
    )


# Importa e adiciona os routers diretamente (evita problemas de importação duplicada)
_rotas_registradas = False

def _registrar_rotas():
    """Registra os routers da API. Esta função evita importações duplicadas."""
    global _rotas_registradas

    if _rotas_registradas:
        return

    from pedidos.api.produtos_api import router as produtos_router
    from pedidos.api.categorias_api import router as categorias_router
    from contas.api.usuario_api import router as usuario_router
    from contas.api.auth_api import auth_router

    api.add_router("/produtos/", produtos_router, auth=jwt_auth)
    api.add_router("/categorias/", categorias_router, auth=jwt_auth)
    api.add_router("/autenticacao/", auth_router)
    api.add_router("/usuario/", usuario_router)

    _rotas_registradas = True


# Registra os routers
_registrar_rotas()
