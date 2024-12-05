"""The fix model in this application."""

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_stubs_ext.db.models import TypedModelMeta

from .future import Future


class Fix(TimeStampedModel, models.Model):  # type: ignore[misc]
    """The fix model."""

    name = models.CharField(max_length=255)
    docstring = models.TextField()
    category = models.CharField(max_length=255)
    future = models.ForeignKey(Future, on_delete=models.CASCADE)

    class Meta(TypedModelMeta):
        constraints = [
            models.UniqueConstraint(fields=["name", "future"], name="unique_fix")
        ]
        verbose_name_plural = "Fixes"

    def __str__(self):
        return "{} object ({}, Future {})".format(
            self.__class__.__name__,
            self.name,
            self.future.version,
        )
