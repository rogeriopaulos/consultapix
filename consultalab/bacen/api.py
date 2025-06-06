import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class BacenRequestApi:
    def __init__(self):
        self.base_url = settings.BACEN_API_DICT_BASEURL
        self.informes_url = settings.BACEN_API_INFORMES

        self.username = settings.BACEN_API_DICT_USER
        self.password = settings.BACEN_API_DICT_PASSWORD

        self.headers = {
            "Accept": "application/json",
        }

        self.pix_endpoint = "/consultar-vinculos-pix"

        self.TIMEOUT_REQUEST = 60  # seconds

    def _execute_pix_request(self, payload: dict) -> dict:
        url = f"{self.base_url}{self.pix_endpoint}"
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=payload,
                auth=(self.username, self.password),
                timeout=self.TIMEOUT_REQUEST,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": str(e),
            }

        return {"status": "success", "data": response.json()}

    def get_pix_by_cpf_cnpj(self, cpf: str, reason: str) -> dict:
        payload = {"cpfCnpj": cpf, "motivo": reason}
        return self._execute_pix_request(payload)

    def get_pix_by_key(self, key: str, reason: str) -> dict:
        payload = {"chave": key, "motivo": reason}
        return self._execute_pix_request(payload)

    def get_bank_info(self, cnpj: str) -> dict:
        """
        Obtém informações bancárias de um CNPJ usando a API de Informes do Bacen.
        """
        try:
            response = requests.get(
                f"{self.informes_url}/pessoasJuridicas",
                params={"cnpj": cnpj},
                timeout=self.TIMEOUT_REQUEST,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            logger.exception("Erro ao obter informações do banco")
            return {}

        return response.json()
