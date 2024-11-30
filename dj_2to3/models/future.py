"""The future model in this application."""

from django.db import models
from django_extensions.db.models import TimeStampedModel
from versionfield import VersionField


class Future(TimeStampedModel, models.Model):  # type: ignore[misc]
    """The future model."""

    version = VersionField(primary_key=True)
