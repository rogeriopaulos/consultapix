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

        self.bank_infos = {}

        self.TIMEOUT_REQUEST = 60  # seconds
        self.STATUS_CODE_SUCCESS = 200

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

        if response.status_code == self.STATUS_CODE_SUCCESS:
            data = response.json()

            chaves = [data]
            if "vinculosPix" in data:
                chaves = data.get("vinculosPix")

            for chave in chaves:
                participante_chave = chave.get("participante")
                if participante_chave is not None:
                    self._save_bank_info(participante_chave)
                    chave["participante"] = self.bank_infos[participante_chave]

                for evento in chave.get("eventosVinculo", []):
                    participante_evento = evento.get("participante")
                    if participante_evento is not None:
                        self._save_bank_info(participante_evento)
                        evento["participante"] = self.bank_infos[participante_evento]

        return {
            "status": "success",
            "data": chaves,
        }

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

    def _save_bank_info(self, participante: str) -> dict:
        if participante not in self.bank_infos:
            bank_info = self.get_bank_info(participante)
            self.bank_infos[participante] = {
                "cnpj": bank_info.get("cnpj", None),
                "nome": bank_info.get("nome", None),
                "codigoCompensacao": bank_info.get("codigoCompensacao", None),
            }
