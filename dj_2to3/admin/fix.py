"""The admin of the model of Fix."""

from typing import Optional

from django.contrib import admin
from django.http import HttpRequest

from ..models import Fix


@admin.register(Fix)
class FixAdmin(
    admin.ModelAdmin[Fix]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The admin of the model of Fix."""

    fieldsets = (
        (None, {"fields": ("name", "future", "category")}),
        ("Docstring", {"fields": ("docstring",)}),
        ("Time", {"fields": ("created", "modified")}),
    )
    list_display = ("name", "future__version", "category", "created", "modified")
    list_filter = ("category",)
    readonly_fields = ("created", "modified")

    def has_add_permission(
        self,
        request: HttpRequest,
        obj: Optional[Fix] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the add permission."""
        return False

    def has_change_permission(
        self,
        request: HttpRequest,
        obj: Optional[Fix] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the change permission."""
        return False

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Optional[Fix] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the delete permission."""
        return False
