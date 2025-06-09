import logging

from celery import shared_task

from consultalab.bacen.api import BacenRequestApi
from consultalab.bacen.helpers import clean_chave_pix_data
from consultalab.bacen.models import ChavePix
from consultalab.bacen.models import RequisicaoBacen

logger = logging.getLogger(__name__)


@shared_task(name="request_bacen_pix")
def request_bacen_pix(requisicao_id: int) -> dict:
    """
    Tarefa Celery para buscar informações de PIX por CPF ou CNPJ.
    """
    requisicao = RequisicaoBacen.objects.get(id=requisicao_id)
    value = requisicao.termo_busca
    reason = requisicao.motivo

    if not value and not reason:
        logger.error("Um valor e um motivo devem ser informados.")
        return {
            "status": "error",
            "message": "Um valor e um motivo devem ser informados.",
        }

    logger.info("Iniciando busca de PIX por CPF/CNPJ: %s", value)

    response = BacenRequestApi().get_pix_by_cpf_cnpj(value, reason)

    if response.get("status") != "success":
        logger.error(response.get("message", "Erro desconhecido"))
        return {
            "status": response.get("status", "error"),
            "message": response.get("message", "Erro desconhecido"),
        }

    logger.info("Tarefa de busca de PIX por CPF/CNPJ concluída")

    chaves = response.get("data", [])
    [create_chave_pix(chave, requisicao) for chave in chaves]

    return {
        "status": "success",
        "message": "Dados de busca de PIX por CPF/CNPJ processados com sucesso",
    }


def create_chave_pix(chave: dict, requisicao: RequisicaoBacen) -> None:
    clean_data = clean_chave_pix_data(chave)
    clean_data["requisicao_bacen"] = requisicao
    eventos = clean_data.pop("eventos_vinculo", [])

    chave_pix = ChavePix.objects.create(**clean_data)

    for evento in eventos:
        chave_pix.eventos_vinculo.create(**evento)
