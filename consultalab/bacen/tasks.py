import logging

from celery import shared_task

from consultalab.bacen.helpers import BacenRequestApi
from consultalab.bacen.models import RequisicaoBacen  # ChavePix, EventoVinculo

logger = logging.getLogger(__name__)


@shared_task(name="request_pix_by_cpfcnpj")
def request_pix_by_cpfcnpj(value: str, reason: str, requisicao_id: int) -> dict:
    """
    Tarefa Celery para buscar informações de PIX por CPF ou CNPJ.
    """
    if not value:
        logger.error("Valor vazio fornecido para busca de PIX por CPF/CNPJ")
        return {
            "status": "error",
            "message": "Valor vazio fornecido para busca de PIX por CPF/CNPJ",
        }

    logger.info(f"Iniciando busca de PIX por CPF/CNPJ: {value}")
    response = BacenRequestApi().request_pix_by_cpfcnpj(value, reason)
    if not response.status == 200:
        return {
            "status": "error",
            "message": response.message,
        }
    logger.info("Tarefa de busca de PIX por CPF/CNPJ concluída")

    requisicao = RequisicaoBacen.objects.get(id=requisicao_id)

    return {
        "status": "success",
        "message": "Dados de busca de PIX por CPF/CNPJ salvos com sucesso",
    }
