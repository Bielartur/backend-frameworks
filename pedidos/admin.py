from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Prefetch

from .models import Categoria, Produto, Pedido, ItensPedido


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)
    ordering = ("nome",)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "categoria", "preco", "ativo", "criado_em")
    list_filter = ("categoria", "ativo")
    search_fields = ("nome", "descricao")
    list_editable = ("ativo",)
    ordering = ("-criado_em",)
    readonly_fields = ("criado_em", "atualizado_em")
    fieldsets = (
        ("Informações do item", {
            "fields": ("nome", "descricao", "preco", "categoria", "imagem", "ativo")
        }),
        ("Datas", {
            "fields": ("criado_em", "atualizado_em"),
            "classes": ("collapse",)
        }),
    )


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "itens_resumo", "status", "criado_em")
    list_filter = ("status", "criado_em", "itens")  # M2M no filtro é permitido, só atenção a performance
    search_fields = ("usuario__email", "itens__nome")
    ordering = ("-criado_em",)
    readonly_fields = ("criado_em",)
    list_editable = ("status",)
    autocomplete_fields = ("usuario", "itens")  # agora vai funcionar

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Prefetch do through para evitar N+1
        return qs.select_related("usuario").prefetch_related(
            "itens",
            Prefetch(
                "itens_pedido",
                queryset=ItensPedido.objects.select_related("produto")
            ),
        )

    def itens_resumo(self, obj):
        itens = obj.itens_pedido.all()
        if not itens:
            return "-"
        linhas = "<br>".join(f"{ip.produto.nome} ×{ip.quantidade}" for ip in itens)
        return format_html(linhas)

    itens_resumo.short_description = "Itens"
