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
]

urlpatterns += htmx_urlpatterns
