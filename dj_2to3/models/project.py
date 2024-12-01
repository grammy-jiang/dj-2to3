"""The project model in this application."""

from pathlib import Path

from django.db import models
from django_extensions.db.models import TimeStampedModel


class Project(TimeStampedModel, models.Model):  # type: ignore[misc]
    """The project model."""

    path = models.FilePathField(
        path=str(Path.home() / "projects"),
        recursive=False,
        allow_files=False,
        allow_folders=True,
        primary_key=True,
    )
