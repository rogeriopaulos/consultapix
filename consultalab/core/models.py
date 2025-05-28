import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from consultalab.core.querysets import AppModelCustomQuerySet


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
