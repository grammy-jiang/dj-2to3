"""The admin of the model of Future."""

from django.contrib import admin

from ..models import Future


@admin.register(Future)
class FutureAdmin(
    admin.ModelAdmin[Future]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The Future admin."""
