import logging

from celery import shared_task

from consultalab.bacen.api import BacenRequestApi
from consultalab.bacen.helpers import clean_chave_pix_data
from consultalab.bacen.models import ChavePix
from consultalab.bacen.models import RequisicaoBacen

logger = logging.getLogger(__name__)


class TaskFailureError(Exception):
    pass


@shared_task(name="request_bacen_pix")
def request_bacen_pix(requisicao_id: int) -> dict:
    """
    Tarefa Celery para buscar informações de PIX por CPF ou CNPJ.
    """
    requisicao = RequisicaoBacen.objects.get(id=requisicao_id)
    value = requisicao.termo_busca
    reason = requisicao.motivo

    if not value and not reason:
        msg = "Nenhum valor ou motivo fornecido para a busca de PIX."
        logger.error(msg)
        raise TaskFailureError(msg)

    logger.info("Iniciando consulta na API do Bacen...")
    api = BacenRequestApi()
    if requisicao.tipo_requisicao == "1":
        search_type = "CPF/CNPJ"
        response = api.get_pix_by_cpf_cnpj(value, reason)
    else:
        search_type = "chave"
        response = api.get_pix_by_key(value, reason)

    logger.info("Concluído busca de PIX por %s: %s", search_type, value)

    if response.get("status") != "success":
        raise TaskFailureError(response.get("message", "Erro desconhecido"))

    logger.info('Tarefa de busca de PIX do valor "%s" concluída com sucesso.', value)

    chaves = response.get("data", [])
    [create_chave_pix(chave, requisicao) for chave in chaves]

    return {
        "status": "success",
        "message": f"Busca de PIX por {search_type} processada com sucesso",
        "search": value,
    }


def create_chave_pix(chave: dict, requisicao: RequisicaoBacen) -> None:
    clean_data = clean_chave_pix_data(chave)
    clean_data["requisicao_bacen"] = requisicao
    eventos = clean_data.pop("eventos_vinculo", [])

    chave_pix = ChavePix.objects.create(**clean_data)

    for evento in eventos:
        chave_pix.eventos_vinculo.create(**evento)
