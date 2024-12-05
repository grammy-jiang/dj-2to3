"""The admin of the model of Future."""

from typing import Optional

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

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
    fieldsets = (
        (None, {"fields": ("version",)}),
        ("Time", {"fields": ("created", "modified")}),
    )
    list_display = ("version", "created", "modified")
    inlines = [
        FixInline,
        PythonExecutableInline,
    ]
    readonly_fields = ("created", "modified")

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

    def has_change_permission(
        self,
        request: HttpRequest,
        obj: Optional[Future] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the change permission."""
        return False
