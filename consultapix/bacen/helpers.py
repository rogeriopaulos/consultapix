import logging

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


class BacenRequestApi:
    def __init__(self):
        self.base_url = settings.BACEN_API_DICT_BASEURL
        self.username = settings.BACEN_API_DICT_USER
        self.password = settings.BACEN_API_DICT_PASSWORD
        self.headers = {
            "Accept": "application/json",
        }
        self.pix_endpoint = "/consultar-vinculos-pix"
        self.TIMEOUT_REQUEST = 60  # seconds

    def _execute_request(self, payload: dict) -> dict:
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
            return {"error": str(e)}

        return response.json()

    def get_pix_by_cpf_cnpj(self, cpf: str, reason: str) -> dict:
        payload = {"cpfCnpj": cpf, "motivo": reason}
        return self._execute_request(payload)

    def get_pix_by_key(self, key: str, reason: str) -> dict:
        payload = {"chave": key, "motivo": reason}
        return self._execute_request(payload)


def camelcase_to_snake_case(data: dict) -> dict:
    """
    Convert camelCase keys in a dictionary to snake_case.
    """

    def camel_to_snake(name: str) -> str:
        return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip(
            "_",
        )

    return {camel_to_snake(k): v for k, v in data.items()}


def has_object(classmodel, **kwargs) -> bool:
    try:
        classmodel.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return False
    else:
        return True
