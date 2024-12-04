"""The project_fix model in this application."""

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_stubs_ext.db.models import TypedModelMeta


class ProjectFix(TimeStampedModel, models.Model):  # type: ignore[misc]
    """The project_fix model."""

    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    fix = models.ForeignKey("Fix", on_delete=models.CASCADE)

    diff = models.TextField()

    class Meta(TypedModelMeta):
        """The Meta class for ProjectFix."""

        verbose_name_plural = "Project Fixes"
        constraints = [
            models.UniqueConstraint(
                fields=["project", "fix"], name="unique_project_fix"
            )
        ]
