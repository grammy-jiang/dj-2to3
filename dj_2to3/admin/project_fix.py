"""The admin of the models about Python."""

from typing import Optional

from pygments import highlight
from pygments.formatters import HtmlFormatter  # pylint: disable=no-name-in-module
from pygments.lexers import DiffLexer  # pylint: disable=no-name-in-module

from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html

from ..models import ProjectFix


@admin.register(ProjectFix)
class ProjectFixAdmin(
    admin.ModelAdmin[ProjectFix]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The PythonExecutable admin."""

    fieldsets = (
        (None, {"fields": ("project", "fix")}),
        ("Syntax Highlight Diff", {"fields": ("syntax_highlight_diff",)}),
        ("Time", {"fields": ("created", "modified")}),
    )
    list_display = ("project", "fix__name", "created", "modified")
    readonly_fields = ("syntax_highlight_diff", "created", "modified")

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

    @admin.display(description="Diff")
    def syntax_highlight_diff(self, obj: ProjectFix) -> str | None:
        """Return the syntax highlight diff."""
        diff = highlight(
            obj.diff,
            DiffLexer(),
            HtmlFormatter(nobackground=True, noclasses=True),
        )
        return format_html(diff)
