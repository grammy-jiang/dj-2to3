"""The admin of the models about Python."""

from typing import Optional

from django.contrib import admin
from django.http import HttpRequest

from ..models import ProjectFix


@admin.register(ProjectFix)
class ProjectFixAdmin(
    admin.ModelAdmin[ProjectFix]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The PythonExecutable admin."""

    list_display = ("project", "fix__name", "created", "modified")
    readonly_fields = ("created", "modified")

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Disable the add permission."""
        return False

    def has_change_permission(
        self,
        request: HttpRequest,
        obj: Optional[ProjectFix] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the change permission."""
        return False

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Optional[ProjectFix] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the delete permission."""
        return False
