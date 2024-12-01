"""The project model in this application."""

from pathlib import Path

import git

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

    def is_git_repository(self) -> bool:
        """Check if the project is a git repository."""
        try:
            git.Repo(self.path).git_dir
        except git.exc.InvalidGitRepositoryError:
            return False
        return True
