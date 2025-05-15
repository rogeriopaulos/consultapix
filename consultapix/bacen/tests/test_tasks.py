import time

import pytest
from celery.result import AsyncResult

from consultapix.bacen.models import ChavePix
from consultapix.bacen.models import RequisicaoBacen
from consultapix.bacen.tasks import request_pix_by_cpfcnpj

pytestmark = pytest.mark.django_db


def test_request_pix_by_cpfcnpj(settings, requisicao_bacen_cpf: RequisicaoBacen):
    task_result = request_pix_by_cpfcnpj.delay(requisicao_bacen_cpf.termo_busca)
    assert isinstance(task_result, AsyncResult)

    # Polling para aguardar o resultado da task
    timeout = 30  # Tempo limite em segundos
    interval = 1  # Intervalo entre verificações
    elapsed_time = 0
    while not task_result.ready() and elapsed_time < timeout:
        time.sleep(interval)
        elapsed_time += interval
    assert task_result.ready(), "A task não foi concluída dentro do tempo limite"

    chave = ChavePix.objects.filter(
        requisicao_bacen=requisicao_bacen_cpf,
        cpf_cnpj=requisicao_bacen_cpf.termo_busca,
    ).first()
    assert chave is not None, "Chave não encontrada no banco de dados"
