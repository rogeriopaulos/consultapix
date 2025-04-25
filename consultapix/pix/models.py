from django.db import models

from consultapix.core.models import AppModel
from consultapix.core.models import EventosVinculo
from consultapix.core.models import RequisicaoBacen


class RequisicaoPixCpfCnpj(AppModel):
    requisicao = models.ForeignKey(
        RequisicaoBacen,
        on_delete=models.CASCADE,
        related_name="pix_cpf_cnpj",
        verbose_name="Requisição Bacen",
    )

    class Meta:
        verbose_name = "Requisição Pix CPF/CNPJ"
        verbose_name_plural = "Requisições Pix CPF/CNPJ"
        db_table = "REQUISICOES_PIX_CPFCNPJ"

    def __str__(self):
        return f"Requisição Pix CPF/CNPJ {self.id} - {self.created}"


class EventoVinculoPixCpfCnpj(EventosVinculo):
    requisicao = models.ForeignKey(
        RequisicaoPixCpfCnpj,
        on_delete=models.CASCADE,
        related_name="eventos_vinculo",
        verbose_name="Requisição Pix CPF/CNPJ",
    )

    class Meta:
        verbose_name = "Evento Vinculo Pix CPF/CNPJ"
        verbose_name_plural = "Eventos Vinculo Pix CPF/CNPJ"
        db_table = "EVENTOS_VINCULO_PIX_CPFCNPJ"

    def __str__(self):
        return f"Evento Vinculo {self.evento} - {self.requisicao}"


class RequisicaoPixChave(AppModel):
    requisicao = models.ForeignKey(
        RequisicaoBacen,
        on_delete=models.CASCADE,
        related_name="pix_chave",
        verbose_name="Requisição Bacen",
    )

    class Meta:
        verbose_name = "Requisição Pix Chave"
        verbose_name_plural = "Requisições Pix Chave"
        db_table = "REQUISICOES_PIX_CHAVE"

    def __str__(self):
        return f"Requisição Pix Chave {self.id} - {self.created}"


class EventoVinculoPixChave(EventosVinculo):
    requisicao = models.ForeignKey(
        RequisicaoPixChave,
        on_delete=models.CASCADE,
        related_name="eventos_vinculo",
        verbose_name="Requisição Pix Chave",
    )

    class Meta:
        verbose_name = "Evento Vinculo Pix Chave"
        verbose_name_plural = "Eventos Vinculo Pix Chave"
        db_table = "EVENTOS_VINCULO_PIX_CHAVE"

    def __str__(self):
        return f"Evento Vinculo {self.evento} - {self.requisicao}"
