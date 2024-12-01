"""The admin of the model of Future."""

from typing import Optional

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from ..models import Future, PythonExecutable


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

    actions = ["create_fixes"]
    list_display = ("version", "created", "modified")
    inlines = [
        PythonExecutableInline,
    ]
    readonly_fields = ("created", "modified")

    @admin.action(description="Create Fixes")
    def create_fixes(self, request: HttpRequest, queryset: QuerySet[Future]) -> None:
        """Create fixes."""
        for future in queryset:
            future.create_fixes()
