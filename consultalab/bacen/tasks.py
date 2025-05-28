import logging
import time

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="request_pix_by_cpfcnpj")
def request_pix_by_cpfcnpj(cpf):
    logger.info("Iniciando tarefa de busca de PIX por CPF/CNPJ")
    time.sleep(10)
    logger.info("Tarefa de busca de PIX por CPF/CNPJ concluída")
    return {
        "status": "success",
        "message": "Busca de PIX por CPF/CNPJ concluída com sucesso",
    }
