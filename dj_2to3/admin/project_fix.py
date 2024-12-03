"""The admin of the models about Python."""

from django.contrib import admin

from ..models import ProjectFix


@admin.register(ProjectFix)
class ProjectFixAdmin(
    admin.ModelAdmin[ProjectFix]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The PythonExecutable admin."""
