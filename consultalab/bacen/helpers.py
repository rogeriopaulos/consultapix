import logging
from datetime import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

logger = logging.getLogger(__name__)


def has_object(classmodel, **kwargs) -> bool:
    try:
        classmodel.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return False
    else:
        return True


def parse_datetime_br(date_str: str) -> datetime | None:
    if not date_str:
        return None

    try:
        dt = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S").astimezone()
    except ValueError:
        try:
            dt = datetime.fromisoformat(date_str)
        except ValueError:
            return None

    if settings.USE_TZ and dt.tzinfo is None:
        dt = timezone.make_aware(dt, timezone.get_default_timezone())

    return dt


def camelcase_to_snake_case(data: dict) -> dict:
    def camel_to_snake(name: str) -> str:
        return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip(
            "_",
        )

    return {camel_to_snake(k): v for k, v in data.items()}


def clean_chave_pix_data(chave: dict) -> dict:
    chave_pix_data = {
        "chave": chave.get("chave"),
        "tipo_chave": chave.get("tipoChave"),
        "status": chave.get("status"),
        "data_abertura_reivindicacao": parse_datetime_br(
            chave.get("dataAberturaReivindicacao"),
        ),
        "cpf_cnpj": chave.get("cpfCnpj"),
        "nome_proprietario": chave.get("nomeProprietario"),
        "nome_fantasia": chave.get("nomeFantasia"),
        "participante": chave.get("participante"),
        "agencia": chave.get("agencia"),
        "numero_conta": chave.get("numeroConta"),
        "tipo_conta": chave.get("tipoConta"),
        "data_abertura_conta": parse_datetime_br(chave.get("dataAberturaConta")),
        "proprietario_da_chave_desde": parse_datetime_br(
            chave.get("proprietarioDaChaveDesde"),
        ),
        "data_criacao": parse_datetime_br(chave.get("dataCriacao")),
        "ultima_modificacao": parse_datetime_br(chave.get("ultimaModificacao")),
    }
    chave_pix_data = {k: v for k, v in chave_pix_data.items() if v is not None}
    chave_pix_data["eventos_vinculo"] = []

    for vinculo in chave.get("eventosVinculo", []):
        if vinculo:
            evento_data = {
                "tipo_evento": vinculo.get("tipoEvento", None),
                "motivo_evento": vinculo.get("motivoEvento", None),
                "data_evento": parse_datetime_br(vinculo.get("dataEvento", None)),
                "chave": vinculo.get("chave", None),
                "tipo_chave": vinculo.get("tipoChave", None),
                "cpf_cnpj": vinculo.get("cpfCnpj", None),
                "nome_proprietario": vinculo.get("nomeProprietario", None),
                "nome_fantasia": vinculo.get("nomeFantasia", None),
                "participante": vinculo.get("participante", None),
                "agencia": vinculo.get("agencia", None),
                "numero_conta": vinculo.get("numeroConta", None),
                "tipo_conta": vinculo.get("tipoConta", None),
                "data_abertura_conta": parse_datetime_br(
                    vinculo.get("dataAberturaConta", None),
                ),
            }
            evento_data = {k: v for k, v in evento_data.items() if v is not None}
            chave_pix_data["eventos_vinculo"].append(evento_data)

    return chave_pix_data
