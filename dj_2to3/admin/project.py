"""The admin of the models about Project."""

from django.contrib import admin

from ..models import Project


@admin.register(Project)
class ProjectAdmin(
    admin.ModelAdmin[Project]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The admin of the models about Project."""

    change_form_template = "dj_2to3/change_form_project.html"
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
