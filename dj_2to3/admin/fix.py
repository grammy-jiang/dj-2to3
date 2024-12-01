"""The admin of the model of Fix."""

from django.contrib import admin

from ..models import Fix


@admin.register(Fix)
class FixAdmin(
    admin.ModelAdmin[Fix]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The admin of the model of Fix."""

    list_display = ("name", "category", "created", "modified")
    list_filter = ("category",)
    readonly_fields = ("created", "modified")
