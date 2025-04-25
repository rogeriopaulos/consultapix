import uuid

from django.contrib.auth import get_user_model
from django.db import models
from model_utils.models import TimeStampedModel

from consultapix.core.querysets import AppModelCustomQuerySet

User = get_user_model()


class AppModel(TimeStampedModel):
    """TimeStampedModel provides self-updating ``created`` and ``modified`` fields"""

    is_void = models.BooleanField("Inativo", default=False, db_column="inativo")
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    objects = AppModelCustomQuerySet.as_manager()

    class Meta:
        abstract = True


class RequisicaoBacen(AppModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="requisicoes_bacen",
        verbose_name="Usuário",
    )
    TIPO_REQUISICAO_CHOICES = [
        ("1", "Pix CPF/CNPJ"),
        ("2", "Pix Chave"),
        ("3", "CCS"),
    ]
    tipo_requisicao = models.CharField(
        max_length=1,
        choices=TIPO_REQUISICAO_CHOICES,
        verbose_name="Tipo de Requisição",
        column_name="tipo_requisicao",
    )

    class Meta:
        verbose_name = "Requisição Bacen"
        verbose_name_plural = "Requisições Bacen"
        db_table = "REQUISICOES_BACEN"

    def __str__(self):
        return f"Requisição {self.tipo_requisicao} | {self.user} | {self.created}"


class EventosVinculo(AppModel):
    evento = models.CharField(max_length=255, verbose_name="Evento")

    class Meta:
        abstract = True
