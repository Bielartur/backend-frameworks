from django.contrib import admin
from .models import Categoria, Produto, Pedido


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
    list_display = ("id", "usuario", "item", "status", "criado_em")
    list_filter = ("status", "criado_em")
    search_fields = ("usuario__email", "item__nome")
    ordering = ("-criado_em",)
    readonly_fields = ("criado_em",)
    list_editable = ("status",)
