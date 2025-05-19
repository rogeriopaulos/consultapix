from django.urls import path

from consultapix.bacen import views

app_name = "bacen"
urlpatterns = [
    path(
        "requisicao/",
        views.RequisicaoBacenCreateView.as_view(),
        name="requisicao_bacen",
    ),
]
htmx_urlpatterns = [
    path("cpf_cnpj/", views.CPFCNPJFormView.as_view(), name="cpf_cnpj"),
    path("chave/", views.ChavePixFormView.as_view(), name="chave"),
    path(
        "processar-requisicao/<int:requisicao_id>/",
        views.ProcessarRequisicaoView.as_view(),
        name="processar_requisicao",
    ),
    path(
        "requisicao/<int:requisicao_id>/status/",
        views.RequisicaoBacenStatusView.as_view(),
        name="requisicao_status",
    ),
    path(
        "requisicao/<int:pk>/",
        views.RequisicaoBacenDetailView.as_view(),
        name="requisicao_bacen_detail",
    ),
]

urlpatterns += htmx_urlpatterns
