from django.contrib import admin

from consultapix.bacen.models import ChavePix
from consultapix.bacen.models import EventoVinculo
from consultapix.bacen.models import RequisicaoBacen


@admin.register(RequisicaoBacen)
class RequisicaoBacenAdmin(admin.ModelAdmin):
    list_display = (
        "termo_busca",
        "tipo_requisicao",
        "motivo",
        "user",
        "processada",
        "created",
    )
    search_fields = ("user__username", "tipo_requisicao", "termo_busca", "motivo")
    list_filter = ("tipo_requisicao", "processada")
    ordering = ("-created",)
    date_hierarchy = "created"


@admin.register(ChavePix)
class ChavePixAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "requisicao_bacen",
        "chave",
        "tipo_chave",
        "status",
    )
    search_fields = ("requisicao_bacen__user__username", "chave", "tipo_chave")
    list_filter = ("status",)
    ordering = ("-created",)
    date_hierarchy = "created"


@admin.register(EventoVinculo)
class EventoVinculoAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "chave",
        "tipo_evento",
        "data_evento",
    )
    search_fields = ("chave",)
    list_filter = ("tipo_evento",)
    ordering = ("-created",)
    date_hierarchy = "created"
