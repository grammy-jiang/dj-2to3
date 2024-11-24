"""The admin of the User model."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from ..models import User


@admin.register(User)
class UserAdmin(_UserAdmin[User]):  # pylint: disable=too-few-public-methods
    """The customized User admin."""

    readonly_fields = ("created", "modified")
