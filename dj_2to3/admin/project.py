"""The admin of the models about Project."""

from typing import Optional

from django.contrib import admin
from django.http import HttpRequest

from ..models import Project, ProjectFix


class ProjectFixInline(
    admin.TabularInline[ProjectFix, Project]
):  # pylint: disable=unsubscriptable-object
    """The inline for the project_fix model."""

    fields = ["fix", "diff", "created", "modified"]
    model = ProjectFix
    readonly_fields = ["created", "modified"]

    def has_add_permission(
        self,
        request: HttpRequest,
        obj: Optional[ProjectFix] = None,  # pylint: disable=unused-argument
    ) -> bool:
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


@admin.register(Project)
class ProjectAdmin(
    admin.ModelAdmin[Project]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The admin of the models about Project."""

    change_form_template = "dj_2to3/change_form_project.html"
    inlines = (ProjectFixInline,)
    list_display = (
        "path",
        "is_git_repository",
        "python_executable__path",
        "created",
        "modified",
    )
    readonly_fields = ("is_git_repository", "created", "modified")

    @admin.display(boolean=True)
    def is_git_repository(self, obj: Project) -> bool:
        """Return whether the project is a git repository."""
        return obj.is_git_repository()
