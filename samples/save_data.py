import json
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model

from consultalab.bacen.helpers import clean_chave_pix_data
from consultalab.bacen.models import ChavePix
from consultalab.bacen.models import RequisicaoBacen

User = get_user_model()

current_dir = settings.BASE_DIR  # PosixPath
pix_cpf_sample = Path(current_dir) / "samples/response_pix_cpf.json"
pix_cnpj_sample = Path(current_dir) / "samples/response_pix_cnpj.json"
pix_chave_sample = Path(current_dir) / "samples/response_pix_chave.json"


def save_data(sample_file, tipo, termo, motivo):
    requisicao = RequisicaoBacen.objects.create(
        user=User.objects.first(),
        tipo_requisicao=tipo,
        termo_busca=termo,
        motivo=motivo,
    )
    with Path.open(sample_file) as file:
        data = json.load(file)

    if tipo == "1":
        [create_chave_pix(item, requisicao) for item in data["vinculosPix"]]
    elif tipo == "2":
        create_chave_pix(data, requisicao)


def create_chave_pix(item, requisicao):
    clean_data = clean_chave_pix_data(item)
    clean_data["requisicao_bacen"] = requisicao
    eventos = clean_data.pop("eventos_vinculo", [])

    chave_pix = ChavePix.objects.create(**clean_data)

    if eventos:
        for evento in eventos:
            chave_pix.eventos_vinculo.create(**evento)


def run():
    save_data(pix_cpf_sample, "1", "00011122233", "Teste CPF")
    save_data(pix_cnpj_sample, "1", "12345678000100", "Teste CNPJ")
    save_data(pix_chave_sample, "2", "00011122233", "Teste Chave")
