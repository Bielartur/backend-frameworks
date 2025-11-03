from django.http import HttpRequest

def get_absolute_media_url(request: HttpRequest, relative_url: str | None) -> str | None:
    """
    Retorna o domínio completo concatenado com a URL relativa da imagem.
    Exemplo: https://meusite.com/media/imagem.png
    """
    if not relative_url:
        return None
    domain = f"{request.scheme}://{request.get_host()}"
    return f"{domain}{relative_url}"