"""The Python executable model in this application."""

from pathlib import Path

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_stubs_ext.db.models import TypedModelMeta


class PythonExecutable(TimeStampedModel, models.Model):  # type: ignore[misc]
    """The Python executable model."""

    path = models.FilePathField(
        path=str(Path.home()),
        match=r"^python[23]\.[0-9]{,2}$",
        recursive=True,
        allow_files=True,
        allow_folders=False,
    )

    class Meta(TypedModelMeta):
        """The Meta class for PythonExecutable."""

        verbose_name = "Python Executable"
