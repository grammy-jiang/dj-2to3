"""The admin of the models about Python."""

from django.contrib import admin

from ..models import PythonExecutable


@admin.register(PythonExecutable)
class PythonExecutableAdmin(
    admin.ModelAdmin[PythonExecutable]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The PythonExecutable admin."""

    list_display = ("path", "version", "created", "modified")
    readonly_fields = ("version", "created", "modified")
