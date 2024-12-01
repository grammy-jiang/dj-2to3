"""The admin of the models about Project."""

from django.contrib import admin

from ..models import Project


@admin.register(Project)
class ProjectAdmin(
    admin.ModelAdmin[Project]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The admin of the models about Project."""

    list_display = ("path", "created", "modified")
    readonly_fields = ("created", "modified")
