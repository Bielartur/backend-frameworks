from ninja import Router
from django.contrib.auth import get_user_model

from core.auth import jwt_auth

User = get_user_model()
router = Router(tags=["Usuário"])

@router.get("/perfil", auth=jwt_auth, summary="Dados do próprio usuário autenticado")
def eu(request):
    return {
        "id": request.user.id,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
    }