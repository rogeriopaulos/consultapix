from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from consultapix.bacen.models import RequisicaoBacen
from consultapix.users.tests.factories import UserFactory


class RequisicaoBacenFactory(DjangoModelFactory[RequisicaoBacen]):
    user = SubFactory(UserFactory)
    tipo_requisicao = Faker("random_element", elements=["1", "2"])
    termo_busca = Faker("cpf", locale="pt_BR")

    class Meta:
        model = RequisicaoBacen
