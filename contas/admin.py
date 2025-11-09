from django.contrib import admin

from contas.models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # defina os campos que fazem sentido para busca
    search_fields = ("email", "nome", "username")