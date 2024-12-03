"""The fix model in this application."""

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_stubs_ext.db.models import TypedModelMeta

from .future import Future


class Fix(TimeStampedModel, models.Model):  # type: ignore[misc]
    """The fix model."""

    name = models.CharField(max_length=255, primary_key=True)
    category = models.CharField(max_length=255)
    future = models.ForeignKey(Future, on_delete=models.CASCADE)

    class Meta(TypedModelMeta):
        verbose_name_plural = "Fixes"
