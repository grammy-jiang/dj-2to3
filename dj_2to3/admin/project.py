"""The admin of the models about Project."""

import html
from typing import Optional

from pygments import highlight
from pygments.formatters import HtmlFormatter  # pylint: disable=no-name-in-module
from pygments.lexers import DiffLexer  # pylint: disable=no-name-in-module

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from ..models import Project, ProjectFix


class ProjectFixInline(
    admin.TabularInline[ProjectFix, Project]
):  # pylint: disable=unsubscriptable-object
    """The inline for the project_fix model."""

    fields = ["fix", "fix_docstring", "syntax_highlight_diff", "created", "modified"]
    model = ProjectFix
    readonly_fields = ["created", "modified", "fix_docstring", "syntax_highlight_diff"]

    @admin.display()
    def fix_docstring(self, obj: ProjectFix) -> str:
        """Return the fix docstring."""
        return obj.fix.docstring

    @admin.display()
    def syntax_highlight_diff(self, obj: ProjectFix) -> str:
        """Return the syntax highlight diff."""
        diff = highlight(
            obj.diff,
            DiffLexer(),
            HtmlFormatter(nobackground=True, noclasses=True),
        )
        safe_diff = html.unescape(diff).replace("{", "{{").replace("}", "}}")
        return format_html(safe_diff)

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

    actions = ("analyze_future",)
    change_form_template = "dj_2to3/admin/change_form_project.html"
    fieldsets = (
        (None, {"fields": ("path", "is_git_repository", "python_executable")}),
        ("Time", {"fields": ("created", "modified")}),
    )
    inlines = (ProjectFixInline,)
    list_display = (
        "path",
        "is_git_repository",
        "python_executable__path",
        "python_executable__future__version",
        "modified",
    )
    list_filter = ("python_executable__path",)
    readonly_fields = ("is_git_repository", "created", "modified")

    @admin.display(boolean=True, description="Is Git Repository")
    def is_git_repository(self, obj: Project) -> bool:
        """Return whether the project is a git repository."""
        return obj.is_git_repository()

    @admin.action(description="Analyze Future")
    def analyze_future(self, request: HttpRequest, queryset: QuerySet[Project]) -> None:
        """Analyze the projects by future."""
        for project in queryset:
            project.analyze_future()

    def has_change_permission(
        self,
        request: HttpRequest,
        obj: Optional[Project] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the change permission."""
        return False
