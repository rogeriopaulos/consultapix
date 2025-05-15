from django.urls import path

from consultapix.bacen.views import ChavePixFormView
from consultapix.bacen.views import CPFCNPJFormView
from consultapix.bacen.views import RequisicaoBacenCreateView

app_name = "bacen"
urlpatterns = [
    path("cpf_cnpj/", CPFCNPJFormView.as_view(), name="cpf_cnpj"),
    path("chave/", ChavePixFormView.as_view(), name="chave"),
    path("requisicao/", RequisicaoBacenCreateView.as_view(), name="requisicao_bacen"),
]
