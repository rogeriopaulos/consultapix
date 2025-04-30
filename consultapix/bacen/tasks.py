import logging
import time

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="request_pix_by_cpf")
def request_pix_by_cpf(cpf):
    logger.info("Iniciando tarefa de busca de PIX por CPF")
    time.sleep(5)
    logger.info("Tarefa de busca de PIX por CPF concluída")
    return {
        "status": "success",
        "message": "Busca de PIX por CPF concluída com sucesso",
    }
