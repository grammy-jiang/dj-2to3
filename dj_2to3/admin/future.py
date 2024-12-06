"""The admin of the model of Future."""

from typing import Optional

from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

from ..models import Fix, Future, PythonExecutable


class FixInline(
    admin.TabularInline[Fix, Future]
):  # pylint: disable=unsubscriptable-object
    """The Fix inline."""

    model = Fix

    def has_add_permission(
        self,
        request: HttpRequest,
        obj: Optional[Fix] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the add permission."""
        return False

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Optional[Fix] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the delete permission."""
        return False

    def has_change_permission(
        self,
        request: HttpRequest,
        obj: Optional[Fix] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the change permission."""
        return False


class PythonExecutableInline(
    admin.StackedInline[PythonExecutable, Future]
):  # pylint: disable=unsubscriptable-object
    """The PythonExecutable inline."""

    model = PythonExecutable

    def has_add_permission(
        self,
        request: HttpRequest,
        obj: Optional[PythonExecutable] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the add permission."""
        return False

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Optional[PythonExecutable] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the delete permission."""
        return False

    def has_change_permission(
        self,
        request: HttpRequest,
        obj: Optional[PythonExecutable] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the change permission."""
        return False


@admin.register(Future)
class FutureAdmin(
    admin.ModelAdmin[Future]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The Future admin."""

    actions = ["load_fixes"]
    change_form_template = "dj_2to3/admin/change_form_future.html"
    fieldsets = (
        (None, {"fields": ("version",)}),
        ("Time", {"fields": ("created", "modified")}),
    )
    list_display = ("version", "created", "modified")
    inlines = [
        FixInline,
        PythonExecutableInline,
    ]
    readonly_fields = ("version", "created", "modified")

    @admin.action(description="Load Fixes")
    def load_fixes(self, request: HttpRequest, queryset: QuerySet[Future]) -> None:
        """Create fixes."""
        for future in queryset:
            future.load_fixes()

    def has_add_permission(
        self,
        request: HttpRequest,
        obj: Optional[Future] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the add permission."""
        return False

    def response_change(self, request: HttpRequest, obj: Future) -> HttpResponse:
        """Override the response_change method."""
        opts = self.opts
        preserved_filters = self.get_preserved_filters(request)
        preserved_qsl = self._get_preserved_qsl(  # type: ignore[attr-defined]
            request, preserved_filters
        )

        msg_dict = {
            "obj_future": format_html(
                '<a href="{}">{}</a>',
                reverse("admin:dj_2to3_future_change", args=[obj.pk]),
                obj,
            ),
        }
        if "_load_fixes" in request.POST:
            fixes = obj.load_fixes()
            msg = format_html(
                _(
                    "The {no_fixes} fixes was loaded successfully from the future "
                    '"{obj_future}".'
                ),
                no_fixes=len(fixes) if fixes else 0,
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
