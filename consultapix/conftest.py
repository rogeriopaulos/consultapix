import pytest

from consultapix.bacen.tests.factories import RequisicaoBacenFactory
from consultapix.users.models import User
from consultapix.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def requisicao_bacen_cpf(db) -> RequisicaoBacenFactory:
    return RequisicaoBacenFactory(tipo_requisicao="1")


@pytest.fixture
def requisicao_bacen_cnpj(db) -> RequisicaoBacenFactory:
    return RequisicaoBacenFactory(tipo_requisicao="1", termo_busca="12345678000100")
