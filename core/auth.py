from ninja_jwt.authentication import JWTAuth


class SlidingJWTAuth(JWTAuth):
    """
    Autenticação JWT customizada para usar SlidingToken.
    Isso garante que os tokens gerados pelo endpoint de login/cadastro
    sejam aceitos pela autenticação dos endpoints protegidos.
    """
    auth_token_classes = ("ninja_jwt.tokens.SlidingToken",)


jwt_auth = SlidingJWTAuth()
