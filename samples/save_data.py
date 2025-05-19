import json
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from consultapix.bacen.models import ChavePix
from consultapix.bacen.models import EventoVinculo
from consultapix.bacen.models import RequisicaoBacen

User = get_user_model()

current_dir = settings.BASE_DIR  # PosixPath
pix_cpf_sample = Path(current_dir) / "samples/response_pix_cpf.json"
pix_cnpj_sample = Path(current_dir) / "samples/response_pix_cnpj.json"
pix_chave_sample = Path(current_dir) / "samples/response_pix_chave.json"


def parse_datetime_br(date_str):
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


def save_chave_pix_data(chave, requisicao):
    # Remove chaves com valores None antes de criar o objeto ChavePix
    chave_pix_data = {
        "requisicao_bacen": requisicao,
        "chave": chave.get("chave", None),
        "tipo_chave": chave.get("tipoChave", None),
        "status": chave.get("status", None),
        "data_abertura_reivindicacao": parse_datetime_br(
            chave.get("dataAberturaReivindicacao", None),
        ),
        "cpf_cnpj": chave.get("cpfCnpj", None),
        "nome_proprietario": chave.get("nomeProprietario", None),
        "nome_fantasia": chave.get("nomeFantasia", None),
        "participante": chave.get("participante", None),
        "agencia": chave.get("agencia", None),
        "numero_conta": chave.get("numeroConta", None),
        "tipo_conta": chave.get("tipoConta", None),
        "data_abertura_conta": parse_datetime_br(chave.get("dataAberturaConta", None)),
        "proprietario_da_chave_desde": parse_datetime_br(
            chave.get("proprietarioDaChaveDesde", None),
        ),
        "data_criacao": parse_datetime_br(chave.get("dataCriacao", None)),
        "ultima_modificacao": parse_datetime_br(chave.get("ultimaModificacao", None)),
    }
    chave_pix_data = {k: v for k, v in chave_pix_data.items() if v is not None}
    chave_pix = ChavePix.objects.create(**chave_pix_data)

    for vinculo in chave.get("eventosVinculo", []):
        evento_data = {
            "chave_pix": chave_pix,
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
        EventoVinculo.objects.create(**evento_data)


def save_data(sample_file, tipo, termo, motivo):
    with Path.open(sample_file) as file:
        requisicao = RequisicaoBacen.objects.create(
            user=User.objects.first(),
            tipo_requisicao=tipo,
            termo_busca=termo,
            motivo=motivo,
        )
        data = json.load(file)
        for item in data["vinculosPix"]:
            save_chave_pix_data(item, requisicao)


def run():
    save_data(pix_cpf_sample, "1", "00011122233", "Teste CPF")
    save_data(pix_cnpj_sample, "1", "12345678000100", "Teste CNPJ")

    with Path.open(pix_chave_sample) as file:
        requisicao = RequisicaoBacen.objects.create(
            user=User.objects.first(),
            tipo_requisicao="2",
            termo_busca="00011122233",
            motivo="Teste Chave",
        )
        data = json.load(file)
        save_chave_pix_data(data, requisicao)
