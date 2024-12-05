"""The project_fix model in this application."""

import subprocess  # nosec B404

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_stubs_ext.db.models import TypedModelMeta


class ProjectFix(TimeStampedModel, models.Model):  # type: ignore[misc]
    """The project_fix model."""

    project = models.ForeignKey("dj_2to3.Project", on_delete=models.CASCADE)
    fix = models.ForeignKey("dj_2to3.Fix", on_delete=models.CASCADE)

    diff = models.TextField()

    class Meta(TypedModelMeta):
        """The Meta class for ProjectFix."""

        verbose_name_plural = "Project Fixes"
        constraints = [
            models.UniqueConstraint(
                fields=["project", "fix"], name="unique_project_fix"
            )
        ]

    def apply_fix(self) -> None:
        """Apply the fix."""
        if not (python_executable := self.project.python_executable):
            return
        subprocess.run(  # nosec B603
            [
                self.fix.future.get_command_path(python_executable),
                "--fix",
                self.fix.name,
                "--write",
                self.project.path,
            ],
            capture_output=True,
            check=True,
            text=True,
        )
