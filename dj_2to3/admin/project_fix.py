"""The admin of the models about Python."""

import html
from typing import Optional
from urllib.parse import quote as urlquote

from pygments import highlight
from pygments.formatters import HtmlFormatter  # pylint: disable=no-name-in-module
from pygments.lexers import DiffLexer  # pylint: disable=no-name-in-module

from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

from ..models import ProjectFix


@admin.register(ProjectFix)
class ProjectFixAdmin(
    admin.ModelAdmin[ProjectFix]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The PythonExecutable admin."""

    change_form_template = "dj_2to3/admin/change_form_project_fix.html"
    fieldsets = (
        (
            None,
            {"fields": ("project", "fix", "fix_name", "fix_category", "fix_docstring")},
        ),
        ("Syntax Highlight Diff", {"fields": ("syntax_highlight_diff",)}),
        ("Time", {"fields": ("created", "modified")}),
    )
    list_display = ("project", "fix__name", "created", "modified")
    list_filter = ("project__path", "fix__category")
    readonly_fields = (
        "project",
        "fix",
        "syntax_highlight_diff",
        "fix_name",
        "fix_category",
        "fix_docstring",
        "created",
        "modified",
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Disable the add permission."""
        return False

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Optional[ProjectFix] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the delete permission."""
        return False

    @admin.display(description="Diff")
    def syntax_highlight_diff(self, obj: ProjectFix) -> str:
        """Return the syntax highlight diff."""
        diff = highlight(
            obj.diff,
            DiffLexer(),
            HtmlFormatter(nobackground=True, noclasses=True),
        )
        safe_diff = html.unescape(diff).replace("{", "{{").replace("}", "}}")
        return format_html(safe_diff)

    @admin.display()
    def fix_name(self, obj: ProjectFix) -> str:
        """Return the fix name."""
        return obj.fix.name

    @admin.display()
    def fix_category(self, obj: ProjectFix) -> str:
        """Return the fix category."""
        return obj.fix.category

    @admin.display()
    def fix_docstring(self, obj: ProjectFix) -> str:
        """Return the fix docstring."""
        return obj.fix.docstring

    def response_change(self, request: HttpRequest, obj: ProjectFix) -> HttpResponse:
        """Handle the response after the change."""
        opts = self.opts
        preserved_filters = self.get_preserved_filters(request)
        preserved_qsl = self._get_preserved_qsl(  # type: ignore[attr-defined]
            request, preserved_filters
        )

        msg_dict = {
            "project__path": obj.project.path,
            "obj": format_html('<a href="{}">{}</a>', urlquote(request.path), obj),
            "obj_fix": format_html(
                '<a href="{}">{}</a>',
                reverse("admin:dj_2to3_fix_change", args=[obj.fix.pk]),
                obj.fix,
            ),
            "obj_project": format_html(
                '<a href="{}">{}</a>',
                reverse("admin:dj_2to3_project_change", args=[obj.project.pk]),
                obj.project,
            ),
        }
        if "_apply_this_fix" in request.POST:
            obj.apply_fix()
            msg = format_html(
                _(
                    'The fix "{obj_fix}" was applied successfully '
                    'on the project "{obj_project}".'
                ),
                **msg_dict,
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters(
                {
                    "preserved_filters": preserved_filters,
                    "preserved_qsl": preserved_qsl,
                    "opts": opts,
                },
                redirect_url,
            )
            return HttpResponseRedirect(redirect_url)

        return super().response_change(request, obj)
